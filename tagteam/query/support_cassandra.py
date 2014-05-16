import re
from cassandra.cluster import Cluster
from post.models import Post, Tag, PostTag

# Get Post from Cassandra db
# input: addset(#ivan) and removeset(#monica) for query: #ivan-#monica
# input: limit the number of posts to displey
# output: Post object in RDBMS
def getposts_ca(addset, removeset, limit):
    """
    Cases:
    
    1) #ivan - #ivan - #school
    Output: [], ERR_MSG -> Nothing to subtract from

    2) #qirong
    Output: [], ERR_MSG -> No such tag found

    3) #qirong - #school
    Output: [], ERR_MSG -> Nothing to subtract from

    4) #qirong + #ivan - #school
    Output: [ << top 10 #ivan - #school >> ], ERR_MSG -> 'Tag(s) not found: qirong'
    """
    # Connect to Cassandra Database
    cluster = Cluster(['localhost'])
#    session = cluster.connect('hash_space')    
 #FIXME using test keyspace 
    session = cluster.connect('test_space')
    # Local Variables
    offset = 0
    pids = set()
    ERR_MSG = ''
    invalid_tags = []
    posts = [] # Return Post objects as the results
    
    # Error check: Empty Query: nothing in addset and removeset
    if not addset and not removeset:
        return [], "Nothing in addset or removeset."

    # Sanitize: Remove all invalid tags in addset and append to error message
    for tag in set(addset):
        try:
            # Get tag count
            result = session.execute("SELECT count(*) from post_tag where tagtext=\'"+tag+"\' limit 10")
            count = result[0].count
            # if count==0, invalid tag query:    
            if count==0:
                invalid_tags.append(tag)
                addset.remove(tag)
        # if retrival of tag fails: invalid query
        except Exception:
            invalid_tags.append(tag)
            addset.remove(tag)

    # Generate error message
    if invalid_tags:
        ERR_MSG = "Tag(s) not found: {0}".format(", ".join(invalid_tags))

    # Case 0: #qirong - #school (Nothing in addset that is left, hence nothing to remove as well)
    # return: empty list with error message as well
    if not addset and invalid_tags:
        return [], ERR_MSG
    
    # ***
    # Accumulated post post_result[]
    post_results = []

    # Flag for empty_result set
    empty_results = False

    # Compile RegEx pattern if there are things in removeset
    if removeset:
        remove_regex = "|".join(removeset)
        pattern = re.compile('#({0})'.format(remove_regex))

    # Iterate to get posts
    while len(post_results) < limit and not empty_results:
        # If no addset items, get recent limit number of posts 
        if not addset:
            # Get limit most recent posts
            # FIXME: Cassandra join all posts, display in descending order
            posts = Post.objects.all().order_by('-id')[offset:offset + limit]

            # Ensure we still have results to process
            if not posts:
                empty_results = True
                continue
        else:
            # Re-initialize pids set
            pids = set()

            # Get limit number of posts for each tags
            for tag in addset:
                # Get list of pids with tag in addset, trim with offset` 
                # FIXME cassandra limit with offset is unknown
                pid=session.execute("select postid from post_tag where tagtext=\'"+tag+"\' order by postid desc limit "+str(limit))
                pid=[p.postid for p in pid]
                pid=pid[offset:offset+limit]

                # Union add the new found pids
                pids = pids.union(set(pid))

            if not len(pids):
                empty_results = True
                continue

            # Get all posts in the pids set
            posts = Post.objects.filter(id__in=pids) 

        # If there are tags to remove, remove them
        if removeset:
            # Remove post that have tags that are present in post.text
            for post in posts:
                if not pattern.findall(post.text):
                    post_results.append(post)
        else:
            post_results = list(posts)

        # Increment offset to get next set of posts
        offset += limit

    #Order posts by id descendingly    
    post_results = sorted(post_results, key=lambda post: -post.id)

    # Get limit number of posts
    post_results = post_results[:limit]

    # Return posts
    return post_results, ERR_MSG


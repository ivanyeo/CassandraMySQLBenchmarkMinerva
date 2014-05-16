from django.test import TestCase
from support_functions import getposts
from post.models import Post, Tag, PostTag
from support_cassandra import getposts_ca
# Create your tests here.
class QuerySupportFunctionTests(TestCase):
    # Static Variables
    setup_complete = False

    def setUp(self):
        if not QuerySupportFunctionTests.setup_complete:
        
            # Data setup section
            Tag.objects.create(value='ivan')
            Tag.objects.create(value='sleeping')
            Tag.objects.create(value='monica')

            Post.objects.create(text='where is #ivan at now?')
            Post.objects.create(text='why is #ivan not #sleeping yet?')
            Post.objects.create(text='what time is #ivan intending to sleep?')
            Post.objects.create(text='hello #monica here')
            Post.objects.create(text='another post from #monica here')

            PostTag.objects.create(pid_id=1, tid_id=1)
            PostTag.objects.create(pid_id=2, tid_id=1)
            PostTag.objects.create(pid_id=2, tid_id=2)
            PostTag.objects.create(pid_id=3, tid_id=1)
            PostTag.objects.create(pid_id=4, tid_id=3)
            PostTag.objects.create(pid_id=5, tid_id=3)

            # Tracking variable section
            QuerySupportFunctionTests.setup_complete = True

    # Case: addset has single item
    def test_single_item_addset(self):
        # 1) Initialize Variables
        addset = set(['ivan'])
        removeset = set()
        
        # 2) Test invocation
        posts, err_msg = getposts_ca(addset, removeset, 10)

        # 3) Get correct posts
        # Initializations
        offset = 0
        limit = 10
        pids = set()

        for tag in addset:
            posttag_set = Tag.objects.get(value=tag).posttag_set.all().order_by('-pid')[offset:offset + limit]
            pids = pids.union({ pt.pid_id for pt in posttag_set })

        # Get all posts to be returned
        posts_correct = Post.objects.filter(id__in=pids) 

        #Order posts by id descendingly    
        posts_correct = sorted(posts_correct, key=lambda post: -post.id)

        # Get limit number of posts
        posts_correct = posts_correct[:limit]

        # 4) Assertions
        #self.assertEqual(len(posts), QuerySupportFunctionTests.total_posts)
        self.assertEqual(set(posts) - set(posts_correct), set())

    # Case: addset has 2 items
    def test_double_item_addset(self):
        # Initialize Variables
        addset = set(['ivan', 'sleeping'])
        removeset = set()
        
        # Test invocation
        posts, err_msg = getposts_ca(addset, removeset, 10)

        # Get correct results for comparison
        offset = 0
        limit = 10
        pids = set()

        for tag in addset:
            posttag_set = Tag.objects.get(value=tag).posttag_set.all().order_by('-pid')[offset:offset + limit]
            pids = pids.union({ pt.pid_id for pt in posttag_set })

        # Get all posts to be returned
        posts_correct = Post.objects.filter(id__in=pids) 

        #Order posts by id descendingly    
        posts_correct = sorted(posts_correct, key=lambda post: -post.id)

        # Get limit number of posts
        posts_correct = posts_correct[:limit]

        # Assertions
        self.assertEqual(len(posts), len(posts_correct))
        self.assertEqual(set(posts) - set(posts_correct), set())

    # Case: addset and removeset BOTH empty
    def test_empty_addset_empty_removeset(self):
        # Initialize Variables
        addset = set()
        removeset = set()
        
        # Test invocation
        posts, err_msg = getposts_ca(addset, removeset, 10)

        # Assertions
        self.assertEqual(err_msg, "Nothing in addset or removeset.")

    # Case: addset has invalid tag, removeset has an item
    # Output: [], Tag(s) not found: qirong
    def test_qirong_addset_school_removeset(self):
        # Initialize Variables
        addset = set(['qirong'])
        removeset = set(['school'])
        
        # Test invocation
        posts, err_msg = getposts_ca(addset, removeset, 10)

        # Assertions
        self.assertEqual(err_msg, "Tag(s) not found: qirong")
        self.assertEqual(posts, [])

    # Case: addset has 1 valid and 1 invalid item, removeset has nothing
    # Output:  posts that contain 'ivan', err_msg: Tag(s) not found: qirong
    def test_ivan_qirong_addset_no_removeset(self):
        # Initialize Variables
        addset = set(['ivan', 'qirong'])
        removeset = set()
        
        # Test invocation
        posts, err_msg = getposts_ca(addset, removeset, 10)

        # Get correct posts
        posts_correct = Post.objects.filter(text__contains='ivan')

        # Assertions
        self.assertEqual(err_msg, "Tag(s) not found: qirong")
        self.assertEqual(set(posts) - set(posts_correct), set())


    # Case: addset has 1 valid and 1 invalid item, removeset has 1 valid item
    # Output:  posts that contain 'ivan' without 'sleeping', err_msg: Tag(s) not found: qirong
    def test_ivan_qirong_addset_sleeping_removeset(self):
        # Initialize Variables
        addset = set(['ivan', 'qirong'])
        removeset = set(['sleeping'])
        
        # Test invocation
        posts, err_msg = getposts_ca(addset, removeset, 10)
        """
        # Get correct posts
        posts_temp = Post.objects.filter(text__contains='ivan')
        posts_correct = []

        for p in posts_temp:
            if not 'sleeping' in p.text:
                posts_correct.append(p)
        """

        # Assertions
        self.assertEqual(err_msg, "Tag(s) not found: qirong")
        #self.assertEqual(set(posts) - set(posts_correct), set())



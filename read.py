# __author__ = 'dimitrios'
from calls import APICalls


class CanvasReader(object):
    """
    Class that contains functions useful for downloading (reading) entities for a course.
    Essentially a wrapper for API get calls for groups of data
    Input always contains a course_id which is a string eg '1112'
    Token that authorises this, has to have access to the course material in order for these to work. ie a professor
    or TA
    (Failure is not currently being handled ie you should handle your own exceptions :)
    """

    def __init__(self, access_token, base_url, api_prefix='/api/v1', verbose=True):
        self.api = APICalls(access_token, base_url + api_prefix, verbose=verbose)

    def get_course_info(self, course_id):
        """
        Returns information about a course
        :param course_id: string eg '1112'
        :return: a dictionary
        dictionary keys: [u'default_view', u'is_public_to_auth_users', u'start_at', u'account_id', u'workflow_state',
        u'restrict_enrollments_to_course_dates', u'storage_quota_mb', u'grading_standard_id', u'public_syllabus',
        u'enrollment_term_id', u'hide_final_grades', u'end_at', u'apply_assignment_group_weights', u'calendar',
        u'enrollments', u'is_public', u'course_code', u'id', u'name']
        """
        return self.api.get('/courses/%s' % course_id, single=True)

    def get_users(self, course_id):
        """
        :param course_id: string eg: '1121'- you must have access to this course material for this to work
        :return: list of dictionaries (one for each user)
        dict has fields [u'sortable_name', u'id', u'short_name', u'name']
        """
        return self.api.get('/courses/%s/users' % course_id)


    def get_student_assignment_submissions(self, course_id, students):
        parameters = {'student_ids': students, 'grouped': True}
        user_submissions = self.api.get('/courses/%s/students/submissions' % course_id, parameters=parameters)
        return user_submissions


    def get_assignments(self, course_id):
        """
        All the assignments in the course
        :param course_id: string
        :return: list of dictionaries
        dict keys [u'has_overrides', u'points_possible', u'updated_at', u'course_id', u'id', u'locked_for_user',
        u'muted', u'moderated_grading', u'grading_type', u'peer_reviews', u'description', u'anonymous_peer_reviews',
         u'grade_group_students_individually', u'grading_standard_id', u'html_url', u'has_submitted_submissions',
         u'group_category_id', u'needs_grading_count', u'unlock_at', u'only_visible_to_overrides', u'name', u'due_at',
         u'created_at', u'post_to_sis', u'lock_at', u'assignment_group_id', u'automatic_peer_reviews', u'published',
         u'position', u'submission_types', u'submissions_download_url', u'unpublishable']
        """
        return self.api.get('/courses/%s/assignments' % course_id)


    def get_assignment_submissions(self, course_id, assignment_id, grouped=False):
        """
        Returns the submissions for a particular assignment
        Only returns those submissions that have actually been submitted, rather than potential submissions.
        :param course_id: string
        :param assignment_id: string
        :return: list of dictionaries (one for each submission)
        dict keys: [u'body', u'user_id', u'submitted_at', u'excused', u'workflow_state', u'url', u'attempt',
        u'preview_url', u'late', u'grade', u'score', u'grade_matches_current_submission', u'grader_id', u'graded_at',
        u'submission_type', u'id', u'assignment_id']
        """
        parameters = {'grouped': grouped}
        submissions = self.api.get('/courses/%s/assignments/%s/submissions' % (course_id, assignment_id),
                                   parameters=parameters)
        return filter(lambda sub: sub['workflow_state'] != 'unsubmitted', submissions)


    def get_assignment_groups(self, course_id):
        """
        Assignements in cavnas are classified intro groups. This returns the info for all such groups
        :param course_id: string
        :return: list of dictionaries with group info
        dictionary keys: [u'group_weight', u'position', u'rules', u'id', u'name']
        """
        return self.api.get('/courses/%s/assignment_groups' % course_id)


    def get_discussion_topics(self, course_id):
        """
        Returns a list of all the topics in the discussion forum in the class
        :param course_id: string
        :return: list of dictionaries - one for each topic
        dictionary keys: [u'attachments', u'delayed_post_at', u'last_reply_at', u'locked_for_user', u'can_group',
        u'url', u'message', u'read_state', u'id', u'unread_count', u'subscribed', u'title', u'discussion_type',
        u'can_unpublish', u'posted_at', u'require_initial_post', u'pinned', u'can_lock', u'allow_rating',
        u'discussion_subentry_count', u'topic_children', u'user_name', u'sort_by_rating', u'root_topic_id',
        u'podcast_has_student_posts', u'podcast_url', u'html_url', u'user_can_see_posts', u'permissions', u'locked',
        u'group_category_id', u'only_graders_can_rate', u'lock_at', u'author', u'assignment_id', u'published',
        u'position']
        """
        return self.api.get('/courses/%s/discussion_topics' % course_id)


    def get_discussion_topic(self, course_id, topic_id):
        """
        Returns information about a specific topic. Single variable is needed here. Most important part is view
        :param course_id: str
        :param topic_id: str
        :return: dictionary
        dictionary keys: [u'new_entries', u'forced_entries', u'unread_entries', u'participants', u'entry_ratings',
        u'view']
        """
        p = dict()
        p['include_new_entries'] = 1
        return self.api.get('/courses/%s/discussion_topics/%s/view' % (course_id, topic_id), single=True, parameters=p)


    def get_student_summary_analytics(self, course_id):
        """
        Returns aggregated analytics for each user.
        :param course_id: string
        :return: list of dicitonaries (one for each student in the course)
        dictionary keys: [u'participations', u'tardiness_breakdown', u'max_page_views', u'max_participations', u'page_views', u'id']
        """
        return self.api.get('/courses/%s/analytics/student_summaries' % course_id)


    def get_student_activity_analytics(self, course_id, user_id):
        """
        Returns a dictionary with two keys 'page views', 'participations'
        Each of those, is a list, with dictionaries which correspond to data points
        :param course_id:
        :param user_id:
        :return:
        """
        return self.api.get('/courses/%s/analytics/users/%s/activity' % (course_id, user_id), single=True)


    def get_participation_analytics(self, course_id):
        return self.api.get('/courses/%s/analytics/activity' % course_id)


    def get_assignment_analytics(self, course_id):
        return self.api.get('/courses/%s/analytics/assignments' % course_id)

from pages.models import Activity, SubmittedActivity, UserAnswer


class AccountManager:
    def __init__(self, user):
        self.user = user

    def validate_new_password(self, old_password, new_password1, new_password2):
        response = {
            'error_code': 0,
            'is_valid': True,
        }
        # check if old password is correct
        if not self.user.check_password(old_password):
            response = {
                'error_code': 1,
                'is_valid': False,
            }
            # check if new passwords match
        elif new_password1 != new_password2:
            response = {
                'error_code': 2,
                'is_valid': False,
            }

        return response

    def get_activity_scores(self):
        activities_submitted = SubmittedActivity.objects.filter(submitted_by=self.user)
        activity_scores = []
        for activity_submitted in activities_submitted:
            correct_answer = UserAnswer.objects.filter(user=self.user, answer__is_correct=True,
                                                       answer__question__activity=activity_submitted.activity).count()
            total = activity_submitted.activity.question_set.count()
            score = {
                'correct_answer': correct_answer,
                'total': total
            }
            activity_scores.append({
                'activity': activity_submitted.activity,
                'score': score
            })
        return activity_scores

    def reset_password(self):
        new_password = self.user.first_name + '.' + self.user.last_name
        self.user.set_password(new_password)
        self.user.save()
        return True


class ActivityManager:
    def __init__(self, activity):
        self.activity = activity



from django.urls import path
from xadminData.views import MeetingDeleteStudent, MeetingAddStudentList, MeetingAddStudent, MeetingImportAddStudent,\
    MeetingImportDeleteStudent, MeetingImportChangeStudent, MeetingImportChangeStudentSave, AllotJurySave, MeetingToAddAllStudent,\
    MeetingJuryAllotAccount, ExportAccount, Download_student_Grade, AddStudentGrade, MeetingChangeStudentGrade, MeetingChangStudentGradeSave,\
    MeetingChangStudentGradeDelete, ExportStatistics, TeacherAllotAccount
app_name = "xadminData"
urlpatterns = [
    path("meetingDeleteStudent/", MeetingDeleteStudent.as_view(), name="meetingDeleteStudent"),
    # 添加学生的学生列表, 用来做局部刷新
    path("meetingAddStudentList/", MeetingAddStudentList.as_view(), name="meetingAddStudentList"),
    # 添加学生
    path("meetingAddStudent/", MeetingAddStudent.as_view(), name="meetingAddStudent"),
    path("meetingAddAllStudent/", MeetingToAddAllStudent.as_view(), name="meetingAddAllStudent"),
    # 添加不符合资格学生
    path("meetingimportAddStudent/", MeetingImportAddStudent.as_view(), name="meetingimportAddStudent"),
    path("meetingImportDeleteStudent/", MeetingImportDeleteStudent.as_view(), name="meetingImportDeleteStudent"),
    path("meetingImportChangeStudent/", MeetingImportChangeStudent.as_view(), name="meetingImportChangeStudent"),
    path("meetingImportChangeSave/", MeetingImportChangeStudentSave.as_view(), name="meetingImportChangeSave"),
    path("allotJurySave/", AllotJurySave.as_view(), name="allotJurySave"),
    # 评委分配账户
    path("allotAccount/", MeetingJuryAllotAccount.as_view(), name="allotAccount"),
    # 导出评委账户
    path("exportAccount/", ExportAccount.as_view(), name="ExportAccount"),
    # 下载学生成绩模板
    path("downloadStudentGradeMuban/", Download_student_Grade.as_view(), name="downloadStudentGradeMuban"),
    path("addStudentGrade/", AddStudentGrade.as_view(), name="addStudentGrade"),
    path("meetingChangeStudentGrade/", MeetingChangeStudentGrade.as_view(), name="meetingChangeStudentGrade"),
    path("meetingChangStudentGradeSave/", MeetingChangStudentGradeSave.as_view(), name="meetingChangStudentGradeSave"),
    path("meetingChangStudentGradeDelete/", MeetingChangStudentGradeDelete.as_view(), name="meetingChangStudentGradeDelete"),
    path("exportStatistics/", ExportStatistics.as_view(), name="exportStatistics"),
    # 分配老师账户
    path("teacherAllotAccount/", TeacherAllotAccount.as_view(), name="teacherAllotAccount"),

]
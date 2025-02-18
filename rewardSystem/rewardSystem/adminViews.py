from xadmin.views import CommAdminView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F
import time, hashlib, os, struct, xlrd, datetime, json
from dataManagement.models import Meeting,AllGrade, File1, Qualification, FuTable, StudentGrade, Jury, ApplicationForm, OtherStudentGrade, Message, MentorGrade, GrantLevel
from MyUser.models import MyUser
from MyUser.task import send_register_active_email


class MeetingManage(CommAdminView):
    def get(self, request):
        context = super().get_context()
        title = "会议设置"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        meeting_title = request.GET.get('_q_')
        # 查询
        if meeting_title:
            meeting_list = Meeting.objects.filter(title__contains=meeting_title).order_by("-id")
            context["q"] = 'yes'
        else:
        # 获取会议列表
            meeting_list = Meeting.objects.all().order_by('-id')
        paginator = Paginator(meeting_list, 30)
        page_num = request.GET.get('page', 1)
        page_of_meetings = paginator.get_page(page_num)
        context["page_of_meetings"] = page_of_meetings


        return render(request, 'meetingManage.html', context)

    # def get_url(self, app_name, stream_name):
    #     t = time.time() + 172800
    #     keytime = str(int(t))
    #     hashstring = "/" + app_name + "/" + stream_name + "-" + keytime + "-0-0-" + app_name + "alipush"
    #     m = hashlib.md5()
    #     m.update(hashstring.encode("utf8"))
    #     mm = m.hexdigest()
    #     print(mm)
    #     push = "rtmp://" + app_name + "alipush.v.myalicdn.com/" + app_name + "/" + stream_name + "?auth_key=" + keytime + "-0-0-" + mm
    #     return push


class MeetingSetting(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "会议设置"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以
        # return render(request, 'test.html', context)  # 最后指定自定义的template模板，并返回context
        meeting_id = request.GET.get('id')
        # id 来进行导入不符合资格学生是绑定会议
        context["meeting_id"] = meeting_id
        #
        meeting_studentinfo_applicationform = []
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        context["meeting"] = meeting_obj
        # get 如果搜索
        _q_ = request.GET.get('_q_')
        if _q_:
            meeting_for_students = meeting_obj.student.filter(Q(sname__contains=_q_) | Q(sno__contains=_q_)).order_by("startDate")
            context["q"] = "q"
        else:
            # 获取参与学生
            meeting_for_students = meeting_obj.student.all().order_by("startDate")
        # 为了会议展示学生是否提交申请表
        for meeting_for_student in meeting_for_students:
            meeting_student_applicationform = meeting_for_student.student_applicationform.filter(meeting=meeting_obj)
            if meeting_student_applicationform:
                meeting_studentinfo_applicationform.append([meeting_for_student, "已提交"])
                # print(meeting_studentinfo_applicationform)
            else:
                meeting_studentinfo_applicationform.append([meeting_for_student, "未提交"])
        context["meeting_students"] = meeting_studentinfo_applicationform
        return render(request, template_name="meetingSetting.html", context=context)


class ImportStudent(CommAdminView):
    def get(self, request):
        context = super().get_context()
        title = "不符合资格学生"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 获取不符合资格学生
        meeting_id = request.GET.get('id')
        meeting = get_object_or_404(Meeting, pk=meeting_id)
        meeting_for_student = meeting.meeting_for_student.all()
        context['meeting_id'] = meeting_id
        context['meeting'] = meeting
        context['meeting_for_student'] = meeting_for_student

        return render(request, template_name="importStudent.html", context=context)

    def post(self, request):
        form_url = request.META.get('HTTP_REFERER', )
        file = request.FILES.get('file')
        id = request.POST.get('pk')
        meeting_obj = get_object_or_404(Meeting, pk=id)
        rexcel = xlrd.open_workbook(filename=None, file_contents=file.read())
        # 获取表格
        sheet = rexcel.sheet_by_index(0)
        row = 1
        while True:
            try:
                rows = sheet.row_values(row)
                objs = Qualification.objects.filter(meeting=meeting_obj, sno=rows[1])
                if not objs:
                    Qualification.objects.create(meeting=meeting_obj, sname=rows[0], sno=rows[1], text=rows[2])
                row += 1
            except IndexError:
                break
        return redirect(form_url)


class Download_student_xls(CommAdminView):

    def get(self, request):
        field = request.GET.get('q')
        if field == "学生信息表":
            file = open(os.getcwd() + '/media/studentMuBan/学生信息模板.xlsx', 'rb')
            file_name = "学生信息表模板"
        elif field == "老师信息表":
            file = open(os.getcwd() + '/media/studentMuBan/老师信息模板.xlsx', 'rb')
            file_name = "老师信息模板"
        else:
            file = open(os.getcwd()+'/media/studentMuBan/student.xlsx', 'rb')
            file_name = "student"
        response = HttpResponse(file)
        response['Content_Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s.xlsx"'%file_name.encode('utf-8').decode('ISO-8859-1')
        # response['Content-Disposition'] = 'attachment;filename="student.xlsx"'

        return response


class AssignTables(CommAdminView):
    def get(self, request):

        context = super().get_context()
        title = "分配赋分表"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 获取 会议列表用来为 select 展示
        meeting_list = Meeting.objects.all()
        # 获取赋分表(赋分表是为学生的申请表关联的)
        fuTable_list = FuTable.objects.all()
        context["meeting_list"] = meeting_list
        context["fuTable_list"] = fuTable_list
        return render(request, template_name="assignTables.html", context=context)

    def post(self, request):
        form_url = request.META.get('HTTP_REFERER', )
        meeting_id = request.POST.get('meeting')
        # 赋分表编号
        futable = request.POST.get("futable")
        # 学号
        studentsno = request.POST.get("studentsno")
        # 姓名
        studentsname = request.POST.get("studentsname")
        if meeting_id and futable:
            meeting = get_object_or_404(Meeting, id=meeting_id)
            if studentsno:
                # 会议中的学生的申请表
                applicationForm_obj = meeting.meeting_for_applicationform.get(sno=studentsno)
                applicationForm_obj.fuTable = get_object_or_404(FuTable, pk=futable)
                applicationForm_obj.save()
            elif studentsname:
                applicationForm_objs = meeting.meeting_for_applicationform.filter(sname=studentsname)
                for applicationForm_obj in applicationForm_objs:
                    applicationForm_obj.fuTable = get_object_or_404(FuTable, pk=futable)
                    applicationForm_obj.save()
            else:
                applicationForm_objs = meeting.meeting_for_applicationform.all()
                for applicationForm_obj in applicationForm_objs:
                    applicationForm_obj.fuTable = get_object_or_404(FuTable, pk=futable)
                    applicationForm_obj.save()

        return redirect(form_url)


# 会议评委列表
class JuryList(CommAdminView):
    def get(self, request):
        context = super().get_context()
        title = "会议评委列表"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        meeting_id = request.GET.get("meeting_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        jury_list = meeting_obj.meeting_jury.all()
        context["meeting_id"] = meeting_obj.id
        context["jury_list"] = jury_list
        context["meeting"] = meeting_obj
        context["meeting_id"] = meeting_obj.id

        return render(request, template_name="JuryList.html", context=context)


# 分配主审评委
class AllotJury(CommAdminView):

    def get(self, request):
        """
        获取当前会议所有赋分表
        获取当前会议所有评委
        :param request:
        :return:
        """
        context = super().get_context()
        title = "分配主评委"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 赋分表和主审老师 applicationform_list_jury = ["赋分表", "主审"]
        applicationform_list_jury = []
        meeting_id = request.GET.get("meeting_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        # 所有赋分表
        applicationform_list = meeting_obj.meeting_for_applicationform.all()
        # 所有评委
        jury_list = meeting_obj.meeting_jury.all()
        # 获取主审
        for applicationform in applicationform_list:
            applicationform_list_jury.append([applicationform, applicationform.jury])
        context["applicationform_list_jury"] = applicationform_list_jury
        context["jury_list"] = jury_list
        context["meeting_id"] = meeting_id
        context["meeting_status"] = meeting_obj.gradeStatus
        return render(request, template_name="AllotJury.html", context=context)

    def post(self, request):
        context = super().get_context()
        title = "分配主评委"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        meeting_id = request.POST.get("meeting_id")
        _q_ = request.POST.get("_q_")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        applicationform_list = meeting_obj.meeting_for_applicationform.filter(Q(sname__contains=_q_) | Q(sno__contains =_q_))
        applicationform_list_jury = []
        # 获取所有评委
        jury_list = meeting_obj.meeting_jury.all()
        for applicationform in applicationform_list:
            applicationform_list_jury.append([applicationform, applicationform.jury])
        context["applicationform_list_jury"] = applicationform_list_jury
        context["jury_list"] = jury_list
        context["meeting_id"] = meeting_id
        context["meeting_status"] = meeting_obj.gradeStatus
        context["q"] = "q"
        return render(request, template_name="AllotJury.html", context=context)


class ImportStudentGrade(CommAdminView):
    def get(self, request):
        context = super().get_context()
        title = "学生成绩"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        meeting_id = request.GET.get("meeting_id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        meeting_student_grade_list = meeting_obj.meeting_student_grade.all()
        context["meeting_id"] = meeting_obj.id
        context["meeting_obj"] = meeting_obj
        context["meeting_student_grade_list"] = meeting_student_grade_list
        return render(request, template_name="importGrade.html", context=context)

    def post(self, request):
        form_url = request.META.get('HTTP_REFERER', )
        file = request.FILES.get('file')
        id = request.POST.get('pk')
        meeting_obj = get_object_or_404(Meeting, pk=id)
        rexcel = xlrd.open_workbook(filename=None, file_contents=file.read())
        # 获取表格
        sheet = rexcel.sheet_by_index(0)
        row = 1
        while True:
            try:
                rows = sheet.row_values(row)
                objs = StudentGrade.objects.filter(meeting=meeting_obj, sno=rows[1])
                if not objs:
                    StudentGrade.objects.create(meeting=meeting_obj, sname=rows[0], sno=rows[1], grade1=rows[2], grade2=rows[3])
                row += 1
            except IndexError:
                break
        return redirect(form_url)


# 后台统计存在的问题例如: 未提交, 未评分等
class StatisticsQuestion(CommAdminView):
    def get(self, request):
        context = super().get_context()
        title = "会议进度"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        meeting_id = request.GET.get("id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        # 获取会议是否有评委未提交
        no_submit_jury = meeting_obj.meeting_jury.filter(all_status="未提交")
        # 导师未评分的
        no_check_applicationForm_list = meeting_obj.meeting_for_applicationform.filter(activity=False)
        # 未参互评的
        noTootherGrade_list = meeting_obj.meeting_for_applicationform.filter(tootherstatus=False)
        # 未被互评的
        nootherGrade_list = meeting_obj.meeting_for_applicationform.filter(otherstatus=False)
        # 未提交的评委
        noSublitJury_list = meeting_obj.meeting_jury.filter(all_status="未提交")
        # 未导入成绩的学生

        context["no_check_applicationForm_list"] = no_check_applicationForm_list
        context["noTootherGrade_list"] = noTootherGrade_list
        context["nootherGrade_list"] = nootherGrade_list
        context["noSublitJury_list"] = noSublitJury_list
        context["meeting_obj"] = meeting_obj

        return render(request, template_name="statisticsQuestion.html", context=context)

    def post(self, request):
        # 1. 提醒老师 2. 提醒学生 3. 提醒评委
        to_user = request.POST.get("username")
        meeting_id = request.POST.get("meeting_id")
        data = request.POST.get("data")
        from_user_obj = get_object_or_404(MyUser, username=request.user.username)
        to_user_obj = get_object_or_404(MyUser, username=to_user)
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        if data.strip() == "1":
            now_date = datetime.datetime.now()
            message_objs = Message.objects.filter(from_user=from_user_obj, to_user=to_user_obj).order_by("-send_time")
            if message_objs:
                days = (now_date-message_objs[0].send_time).days
                if days < 1:
                    return JsonResponse({"status": "今天已提醒"})
                else:
                    text = "在<%s>会议中你有学生未评分." % meeting_obj
                    Message.objects.create(from_user=from_user_obj, to_user=to_user_obj, text=text)
                    if to_user_obj.email:
                        send_register_active_email(to_user_obj.email, text, 1)
                    return JsonResponse({"status": "成功"})
            else:
                text = "在<%s>会议中你有学生未评分."%meeting_obj
                Message.objects.create(from_user=from_user_obj, to_user=to_user_obj, text=text)
                if to_user_obj.email:
                    send_register_active_email(to_user_obj.email, text, 1)
                return JsonResponse({"status": "成功"})
        elif data.strip() == "2":
            now_date = datetime.datetime.now()
            message_objs = Message.objects.filter(from_user=from_user_obj, to_user=to_user_obj).order_by("-send_time")
            if message_objs:
                days = (now_date - message_objs[0].send_time).days
                if days < 1:
                    return JsonResponse({"status": "今天已提醒"})
                else:
                    text = "在<%s>会议中你未参与学生互评!请尽快进行否则将影响你的成绩." % meeting_obj.title
                    Message.objects.create(from_user=from_user_obj, to_user=to_user_obj, text=text)
                    if to_user_obj.email:
                        send_register_active_email(to_user_obj.email, text, 1)
                    return JsonResponse({"status": "成功"})
            else:
                text = "在<%s>会议中你为参与学生互评!请尽快进行否则将影响你的成绩."%meeting_obj.title
                Message.objects.create(from_user=from_user_obj, to_user=to_user_obj, text=text)
                if to_user_obj.email:
                    send_register_active_email(to_user_obj.email, text, 1)
                return JsonResponse({"status": "成功"})
        elif data.strip() == "3":
            now_date = datetime.datetime.now()
            message_objs = Message.objects.filter(from_user=from_user_obj, to_user=to_user_obj).order_by("-send_time")
            if message_objs:
                days = (now_date - message_objs[0].send_time).days
                if days < 1:
                    return JsonResponse({"status": "今天已提醒"})
                else:
                    text = "在<%s>会议中你有学生未评分." % meeting_obj
                    Message.objects.create(from_user=from_user_obj, to_user=to_user_obj, text=text)
                    if to_user_obj.email:
                        send_register_active_email(to_user_obj.email, text, 1)
                    return JsonResponse({"status": "成功"})
            else:
                text = "在<%s>会议中你还未提交评分,请尽快提交." % meeting_obj
                Message.objects.create(from_user=from_user_obj, to_user=to_user_obj, text=text)
                if to_user_obj.email:
                    send_register_active_email(to_user_obj.email, text, 1)
                return JsonResponse({"status": "成功"})
        else:
            return JsonResponse({"status": "存在问题"})


class StatisticsResult(CommAdminView):
    def get(self, request):
        context = super().get_context()
        title = "会议进度"
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        meeting_id = request.GET.get("id")
        meeting_obj = get_object_or_404(Meeting, pk=meeting_id)
        meeting_grade_list = meeting_obj.meetingALLGrade.values("applicationForm").annotate(grade=Sum(F('grade1') + F('grade2') +F('grade3')))
        avg_applicationForm_list = []
        for meeting_grade in meeting_grade_list:
            applicationFormObj = get_object_or_404(ApplicationForm, pk=meeting_grade["applicationForm"])
            allGradeObj = get_object_or_404(AllGrade, applicationForm=applicationFormObj)
            avg_applicationForm_list.append([allGradeObj, meeting_grade["grade"], applicationFormObj.grant.all()])
        context["meeting_obj"] = meeting_obj
        context["avg_applicationForm_list"] = avg_applicationForm_list
        # 奖助等级
        grantLevel_list = GrantLevel.objects.all()
        context["grantLevel_list"] = grantLevel_list

        return render(request, template_name="statisticsResult.html", context=context)

    def post(self, request):
        dataList = request.POST.get("dataList")
        applicationForm_id = json.loads(dataList)[0].split(",")[0]
        applicationForm_obj = get_object_or_404(ApplicationForm, pk=applicationForm_id)
        # 先清空他的等级
        applicationForm_obj.grant.clear()
        # 再添加
        for data in json.loads(dataList):
            applicationForm_id, grant_id = data.split(",")
            applicationForm_obj = get_object_or_404(ApplicationForm, pk=applicationForm_id)
            grant_obj = get_object_or_404(GrantLevel, pk=grant_id)
            applicationForm_obj.grant.add(grant_obj)
        return JsonResponse({"status": "成功"})

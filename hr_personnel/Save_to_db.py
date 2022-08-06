import pandas as pd
import csv
import os
from department.models import Department, DepartmentHod, DepartmentKeyObjective, DepartmentManager, DepartmentTrainee
from numbers_of_days.models import NumbersOfDays
# import pdb


from .models import Batch, HodCreationError, HrPersonnel

from accounts.models import User


class GrabAndSaveToDb:

    def __init__(self, csv_file):
        self.csv_object = csv_file

    def Check_and_save_hod(self):
            # check if epty
            # if epth exist ?
            # return error messsage
            # else
            # pass
        try:
            split_tup = os.path.splitext(str(self.csv_object.csv_file))
            file_extension = split_tup[1]
            if file_extension == '.csv':
                read_csv_file = pd.read_csv(self.csv_object.csv_file, keep_default_na=False).to_dict()
                # print(type(pd.read_csv(self.csv_object.csv_file).isnull().sum()))

                # read_csv_file = pd.read_csv(self.csv_object.csv_file).to_dict()



                trainee_ids = list(read_csv_file['TRAINEE ID'].values())
                trainee_names = list(read_csv_file['TRAINEE NAME'].values())
                trainee_emails = list(read_csv_file['TRAINEE EMAIL'].values())

                manager_ids = list(read_csv_file['MANAGER ID'].values())
                manager_namess = list(read_csv_file['MANAGER NAME'].values())
                manager_emails = list(read_csv_file['MANAGER EMAIL'].values())

                hod_ids = list(read_csv_file['HOD ID'].values())
                hod_names = list(read_csv_file['HOD Name'].values())
                hod_emails = list(read_csv_file['HOD Email'].values())

                departments = list(read_csv_file['Department'].values())
                number_of_days = list(read_csv_file['NUMBER OF DAYS'].values())
                key_objectives = list(read_csv_file['Key Objectives'].values())
                main_department = list(
                    read_csv_file['MAIN DEPARTMENT'].values())

                

                self.save_trainees(trainee_ids, trainee_names, trainee_emails,
                                   departments, number_of_days, key_objectives, main_department)

                self.save_managers(manager_ids, manager_namess,
                                   manager_emails, departments, key_objectives)
                self.save_hod(hod_ids, hod_names, hod_emails,
                              departments, key_objectives)

                return 200

            elif file_extension == '.xlsx' or file_extension == 'xls':
                read_excel_file = pd.read_excel(
                    self.csv_object.csv_file, sheet_name=None).to_dict()
                # data_dict = dfs.to_dict()

                return 200

            else:
                pass

    
        except Exception as e:
            print(e)
            return 400, self.format_error(e)


    # pdb.set_trace()
    def save_managers(self, manager_ids, manager_names, manager_emails, departments, key_objectives):
        # import pdb; pdb.set_trace()
        for manager_id, manager_name, manager_email, department, key_objective in zip(manager_ids, manager_names, manager_emails, departments, key_objectives):
            manager_exists = User.objects.filter(email=manager_email).first()
            department_exists = Department.objects.filter(
                department_name=department.lower().strip()).first()
            manager_department_exists = DepartmentManager.objects.filter(
                department=department_exists, manager=manager_exists).first()
            if manager_exists is not None:
                manager_exists.staff_id=manager_id
                manager_exists.name=manager_name
                manager_exists.email=manager_email
                manager_exists.role='manager'
                batch=self.csv_object
                manager_exists.save()

                if department_exists is not None:
                    if manager_department_exists is not None:
                        # override by editing the manager/departmnt instance that exist and saving with manager and department that exist
                        manager_department_exists.department = department_exists
                        manager_department_exists.manager = manager_exists
                        manager_department_exists.save()

                    else:
                        DepartmentManager.objects.create(
                            department=department_exists,
                            manager=manager_exists
                        )

                else:

                    dept = Department.objects.create(
                        department_name=department.lower().strip(), key_objective=key_objective)
                    self.save_key_objective(
                        department=dept, key_objectives=key_objectives, departments=departments)

                    DepartmentManager.objects.create(
                        department=dept,
                        manager=manager_exists
                    )
            else:
                manager_exists = User.objects.create(
                    staff_id=manager_id, name=manager_name, email=manager_email, role='manager', batch=self.csv_object)
                if department_exists is not None:
                    DepartmentManager.objects.create(
                        department=department_exists,
                        manager=manager_exists
                    )
                else:

                    dept = Department.objects.create(
                        department_name=department.lower().strip(), key_objective=key_objective)
                    self.save_key_objective(
                        department=dept, key_objectives=key_objectives, departments=departments)
                    DepartmentManager.objects.create(
                        department=dept,
                        manager=manager_exists
                    )

    def save_hod(self, hod_ids, hod_names, hod_emails, departments, key_objectives):
        # print(f'all HODS goten {hod_names}')
        for hod_id, hod_name, hod_email, department, key_objective in zip(hod_ids, hod_names, hod_emails, departments, key_objectives):
            hod_exists = User.objects.filter(email=hod_email.strip()).first()
            department_exists = Department.objects.filter(
                department_name=department.lower().strip()).first()
            hod_department_exists = DepartmentHod.objects.filter(
                department=department_exists, hod=hod_exists).last()
            hod_exists_elsewhere = DepartmentHod.objects.filter(
                hod=hod_exists).last()
            # print(f'hod_name on now : {hod_name}', 'HOD exists {hod_exists}')
            
            if hod_exists_elsewhere is not None:
                HodCreationError.objects.create(
                    error_message=f'HOD with Id {hod_exists.id}\
                            , email {hod_exists.email},\
                            already exist in {hod_exists_elsewhere.department}.\
                            and you are trying to add him to {department_exists}\
                            which is not possible',
                    batch=self.csv_object
                )
                pass
                

            # if hod_department_exists is not None:
            #     print('aHOD and dept already exist', hod_name, department)
            #     hod_department_exists.department = department_exists
            #     hod_department_exists.hod = hod_exists
            #     hod_department_exists.save() 
           
            # print('Hit check if hod exists')
            # print(hod_exists, hod_name)
            if hod_exists is not None:
                # print('hod exists I am changing his name')
                hod_exists.name = hod_name
                # print(hod_exists.name)
                hod_exists.email = hod_email.strip()
                # print(hod_exists.email)
                hod_exists.role='hod'
                batch=self.csv_object
                hod_exists.save()
                # print('hod exists I have changed his name', hod_exists.name)
            # else:
            #     print('hod does not exist I am creating him')
            #     hod_exists = User.objects.create(
            #         staff_id=hod_id, name=hod_name, email=hod_email.strip(), role='hod', batch=self.csv_object)

                if department_exists is not None:
                    if hod_department_exists is not None:
                        # print('aHOD and dept already exist', hod_name, department)
                        hod_department_exists.department = department_exists
                        hod_department_exists.hod = hod_exists
                        hod_department_exists.save()
                        # print('department already exists')
                    else:
                        dept_hod = DepartmentHod.objects.create(
                            department=department_exists, hod=hod_exists)
                        # print('department exist joining the dept and hod together', dept_hod)
            
            
                else:
                    # print('hit this last else ')
                    dept = Department.objects.create(
                        department_name=department.lower().strip(), key_objective=key_objective)

                    self.save_key_objective(
                        department=dept, key_objectives=key_objectives, departments=departments)
                    dept_hod = DepartmentHod.objects.create(
                        department=dept, hod=hod_exists)

                    # print(dept_hod, 'this this this')
            else:
                # print(hod_name)
                # print('hod does not exist I am creating him')
                hod_exists = User.objects.create(
                    staff_id=hod_id, name=hod_name, email=hod_email.strip(), role='hod', batch=self.csv_object)

                if department_exists is not None:
                    # print(f'department exist ooooo{department_exists} departmnt')

                    dept_hod = DepartmentHod.objects.create(
                            department=department_exists, hod=hod_exists)
                    # print(dept_hod, 'department hod linked')
                else:
                    # print()
                    # print(f'department does not exist {department} departmnt')
                    department_exists = Department.objects.create(
                        department_name=department.lower().strip(), key_objective=key_objective)
                    dept_hod = DepartmentHod.objects.create(
                            department=department_exists, hod=hod_exists)

    def save_trainees(self, trainees_ids, trainees_names, trainees_emails, departments, number_of_days, key_objectives, main_department):
        for staff_id, trainee_name, trainee_email, department, number_of_day, key_objective, main in zip(trainees_ids, trainees_names, trainees_emails, departments, number_of_days, key_objectives, main_department):
            user_exists = User.objects.filter(email=trainee_email).first()
            department_exists = Department.objects.filter(
                department_name=department.lower()).first()

            user_department_exists = DepartmentTrainee.objects.filter(
                department=department_exists, trainee=user_exists).first()

            if department_exists is not None:
                if user_exists is not None:
                    if user_department_exists is not None:
                        # over write and save
                        user_department_exists.trainee = user_exists
                        user_department_exists.department = department_exists
                        department_exists.save()
                    else:
                        DepartmentTrainee.objects.create(
                            department=department_exists,
                            trainee=user_exists
                        )

                        # department_exists.trainees.add(user_exists)
                        number_of_days = NumbersOfDays.objects.create(
                            value=number_of_day, department=department_exists, trainee=user_exists, main_department=main)
                        number_of_days.save()

                else:

                    trainee = User.objects.create(
                        staff_id=staff_id, name=trainee_name, email=trainee_email, role='trainee', batch=self.csv_object)
                    # department_exists.trainees.add(trainee)
                    DepartmentTrainee.objects.create(
                        department=department_exists,
                        trainee=trainee
                    )
                    number_of_days = NumbersOfDays.objects.create(
                        value=number_of_day, department=department_exists, trainee=trainee, main_department=main)
                    number_of_days.save()
            else:
                dept = Department.objects.create(
                    department_name=department.lower(), key_objective=key_objective)
                self.save_key_objective(
                    department=dept, key_objectives=key_objectives, departments=departments)
                if user_exists is not None:
                    # dept.trainees.add(user_exists)
                    DepartmentTrainee.objects.create(
                        department=dept,
                        trainee=user_exists
                    )
                    number_of_days = NumbersOfDays.objects.create(
                        value=number_of_day, department=dept, trainee=user_exists, main_department=main)
                    number_of_days.save()
                else:

                    trainee = User.objects.create(
                        staff_id=staff_id, name=trainee_name, email=trainee_email, role='trainee', batch=self.csv_object)
                    # dept.trainees.add(trainee)
                    DepartmentTrainee.objects.create(
                        department=dept,
                        trainee=trainee
                    )
                    number_of_days = NumbersOfDays.objects.create(
                        value=number_of_day, department=dept, trainee=trainee, main_department=main)
                    number_of_days.save()

    def save_key_objective(self, department, key_objectives, departments):
        for i in range(len(departments)):
            departments[i] = departments[i].lower()
        try:
            index_of_dept = departments.index(department.department_name)
            key_objective = key_objectives[index_of_dept]
            splitted_key_objective_array = key_objective.split("\n")
            for i in splitted_key_objective_array:
                if i != "":
                    p, created = DepartmentKeyObjective.objects.get_or_create(
                        department=department,
                        key_objective=i,
                    )
                # DepartmentKeyObjective.objects.create(department=department, key_objective=i)
        except Exception as e:
            pass


            
            


    def format_error(self, error_string):
        try:
            template = "An exception of type {0} occurred. Arguments:{1!r}"
            message = template.format(
                type(error_string).__name__, error_string.args)
            return message
            # return
        except Exception as error_string:
            return error_string





















# import pandas as pd
# import csv
# import os
# from department.models import Department, DepartmentHod, DepartmentKeyObjective, DepartmentManager, DepartmentTrainee
# from numbers_of_days.models import NumbersOfDays
# # import pdb


# from .models import Batch, HodCreationError, HrPersonnel

# from accounts.models import User


# class GrabAndSaveToDb:

#     def __init__(self, csv_file):
#         self.csv_object = csv_file

#     def Check_and_save_hod(self):
#             # check if epty
#             # if epth exist ?
#             # return error messsage
#             # else
#             # pass
#         try:
#             split_tup = os.path.splitext(str(self.csv_object.csv_file))
#             file_extension = split_tup[1]
#             if file_extension == '.csv':
#                 read_csv_file = pd.read_csv(self.csv_object.csv_file, keep_default_na=False).to_dict()
#                 # print(type(pd.read_csv(self.csv_object.csv_file).isnull().sum()))

#                 # read_csv_file = pd.read_csv(self.csv_object.csv_file).to_dict()



#                 trainee_ids = list(read_csv_file['TRAINEE ID'].values())
#                 trainee_names = list(read_csv_file['TRAINEE NAME'].values())
#                 trainee_emails = list(read_csv_file['TRAINEE EMAIL'].values())

#                 manager_ids = list(read_csv_file['MANAGER ID'].values())
#                 manager_namess = list(read_csv_file['MANAGER NAME'].values())
#                 manager_emails = list(read_csv_file['MANAGER EMAIL'].values())

#                 hod_ids = list(read_csv_file['HOD ID'].values())
#                 hod_names = list(read_csv_file['HOD Name'].values())
#                 hod_emails = list(read_csv_file['HOD Email'].values())

#                 departments = list(read_csv_file['Department'].values())
#                 number_of_days = list(read_csv_file['NUMBER OF DAYS'].values())
#                 key_objectives = list(read_csv_file['Key Objectives'].values())
#                 main_department = list(
#                     read_csv_file['MAIN DEPARTMENT'].values())

                

#                 self.save_trainees(trainee_ids, trainee_names, trainee_emails,
#                                    departments, number_of_days, key_objectives, main_department)

#                 self.save_managers(manager_ids, manager_namess,
#                                    manager_emails, departments, key_objectives)
#                 self.save_hod(hod_ids, hod_names, hod_emails,
#                               departments, key_objectives)

#                 return 200

#             elif file_extension == '.xlsx' or file_extension == 'xls':
#                 read_excel_file = pd.read_excel(
#                     self.csv_object.csv_file, sheet_name=None).to_dict()
#                 # data_dict = dfs.to_dict()

#                 return 200

#             else:
#                 pass

    
#         except Exception as e:
#             print(e)
#             return 400, self.format_error(e)


#     # pdb.set_trace()
#     def save_managers(self, manager_ids, manager_names, manager_emails, departments, key_objectives):
#         # import pdb; pdb.set_trace()
#         for manager_id, manager_name, manager_email, department, key_objective in zip(manager_ids, manager_names, manager_emails, departments, key_objectives):
#             manager_exists = User.objects.filter(email=manager_email).first()
#             department_exists = Department.objects.filter(
#                 department_name=department.lower().strip()).first()
#             manager_department_exists = DepartmentManager.objects.filter(
#                 department=department_exists, manager=manager_exists).first()
#             if manager_exists is not None:
#                 manager_exists.staff_id=manager_id
#                 manager_exists.name=manager_name
#                 manager_exists.email=manager_email
#                 manager_exists.role='manager'
#                 # batch=self.csv_object
#                 manager_exists.save()

#                 if department_exists is not None:
#                     if manager_department_exists is not None:
#                         # override by editing the manager/departmnt instance that exist and saving with manager and department that exist
#                         manager_department_exists.department = department_exists
#                         manager_department_exists.manager = manager_exists
#                         manager_department_exists.save()

#                     else:
#                         DepartmentManager.objects.create(
#                             department=department_exists,
#                             manager=manager_exists
#                         )

#                 else:

#                     dept = Department.objects.create(
#                         department_name=department.lower().strip(), key_objective=key_objective)
#                     self.save_key_objective(
#                         department=dept, key_objectives=key_objectives, departments=departments)

#                     DepartmentManager.objects.create(
#                         department=dept,
#                         manager=manager_exists
#                     )
#             else:
#                 manager = User.objects.create(
#                     staff_id=manager_id, name=manager_name, email=manager_email, role='manager', batch=self.csv_object)
#                 if department_exists is not None:
#                     DepartmentManager.objects.create(
#                         department=department_exists,
#                         manager=manager
#                     )
#                 else:

#                     dept = Department.objects.create(
#                         department_name=department.lower().strip(), key_objective=key_objective)
#                     self.save_key_objective(
#                         department=dept, key_objectives=key_objectives, departments=departments)
#                     DepartmentManager.objects.create(
#                         department=dept,
#                         manager=manager
#                     )

#     def save_hod(self, hod_ids, hod_names, hod_emails, departments, key_objectives):
#         for hod_id, hod_name, hod_email, department, key_objective in zip(hod_ids, hod_names, hod_emails, departments, key_objectives):
#             # print('start forloop')
#             hod_exists = User.objects.filter(email=hod_email).first()
            
#             department_exists = Department.objects.filter(
#                 department_name=department.lower().strip()).first()
#             hod_department_exists = DepartmentHod.objects.filter(
#                 department=department_exists, hod=hod_exists).last()
#             hod_exists_elsewhere = DepartmentHod.objects.filter(
#                 hod=hod_exists).last()

#             if hod_department_exists is not None:
#                 hod_department_exists.department = department_exists
#                 hod_department_exists.hod = hod_exists
#                 hod_department_exists.save()
#             else:
                
#                 if hod_exists_elsewhere is not None:
#                     HodCreationError.objects.create(
#                         error_message=f'HOD with Id {hod_exists.id}\
#                                 , email {hod_exists.email},\
#                                 already exist in {hod_exists_elsewhere.department}.\
#                                 and you are trying to add him to {department_exists}\
#                                 which is not possible',
#                         batch=self.csv_object
#                     )
#                 else:
#                     if hod_exists is not None:
#                         hod_exists.name = hod_name
#                         hod_exists.email = hod_email
#                         hod_exists.role='hod'
#                         # batch=self.csv_object
#                         hod_exists.save()
#                     else:
#                         hod = User.objects.create(
#                             staff_id=hod_id, name=hod_name, email=hod_email, role='hod', batch=self.csv_object)

#                     if department_exists is not None:
#                         dept_hod = DepartmentHod.objects.create(
#                             department=department_exists, hod=hod)
#                     else:
#                         dept = Department.objects.create(
#                             department_name=department.lower().strip(), key_objective=key_objective)
#                         self.save_key_objective(
#                             department=dept, key_objectives=key_objectives, departments=departments)
#                         dept_hod = DepartmentHod.objects.create(
#                             department=dept, hod=hod)

#     def save_trainees(self, trainees_ids, trainees_names, trainees_emails, departments, number_of_days, key_objectives, main_department):
#         for staff_id, trainee_name, trainee_email, department, number_of_day, key_objective, main in zip(trainees_ids, trainees_names, trainees_emails, departments, number_of_days, key_objectives, main_department):
#             user_exists = User.objects.filter(email=trainee_email).first()
#             department_exists = Department.objects.filter(
#                 department_name=department.lower()).first()

#             user_department_exists = DepartmentTrainee.objects.filter(
#                 department=department_exists, trainee=user_exists).first()

#             if department_exists is not None:
#                 if user_exists is not None:
#                     if user_department_exists is not None:
#                         # over write and save
#                         user_department_exists.trainee = user_exists
#                         user_department_exists.department = department_exists
#                         department_exists.save()
#                     else:
#                         DepartmentTrainee.objects.create(
#                             department=department_exists,
#                             trainee=user_exists
#                         )

#                         # department_exists.trainees.add(user_exists)
#                         number_of_days = NumbersOfDays.objects.create(
#                             value=number_of_day, department=department_exists, trainee=user_exists, main_department=main)
#                         number_of_days.save()

#                 else:

#                     trainee = User.objects.create(
#                         staff_id=staff_id, name=trainee_name, email=trainee_email, role='trainee', batch=self.csv_object)
#                     # department_exists.trainees.add(trainee)
#                     DepartmentTrainee.objects.create(
#                         department=department_exists,
#                         trainee=trainee
#                     )
#                     number_of_days = NumbersOfDays.objects.create(
#                         value=number_of_day, department=department_exists, trainee=trainee, main_department=main)
#                     number_of_days.save()
#             else:
#                 dept = Department.objects.create(
#                     department_name=department.lower(), key_objective=key_objective)
#                 self.save_key_objective(
#                     department=dept, key_objectives=key_objectives, departments=departments)
#                 if user_exists is not None:
#                     # dept.trainees.add(user_exists)
#                     DepartmentTrainee.objects.create(
#                         department=dept,
#                         trainee=user_exists
#                     )
#                     number_of_days = NumbersOfDays.objects.create(
#                         value=number_of_day, department=dept, trainee=user_exists, main_department=main)
#                     number_of_days.save()
#                 else:

#                     trainee = User.objects.create(
#                         staff_id=staff_id, name=trainee_name, email=trainee_email, role='trainee', batch=self.csv_object)
#                     # dept.trainees.add(trainee)
#                     DepartmentTrainee.objects.create(
#                         department=dept,
#                         trainee=trainee
#                     )
#                     number_of_days = NumbersOfDays.objects.create(
#                         value=number_of_day, department=dept, trainee=trainee, main_department=main)
#                     number_of_days.save()

#     def save_key_objective(self, department, key_objectives, departments):
#         for i in range(len(departments)):
#             departments[i] = departments[i].lower()
#         try:
#             index_of_dept = departments.index(department.department_name)
#             key_objective = key_objectives[index_of_dept]
#             splitted_key_objective_array = key_objective.split("\n")
#             for i in splitted_key_objective_array:
#                 if i != "":
#                     p, created = DepartmentKeyObjective.objects.get_or_create(
#                         department=department,
#                         key_objective=i,
#                     )
#                 # DepartmentKeyObjective.objects.create(department=department, key_objective=i)
#         except Exception as e:
#             pass


            
            


#     def format_error(self, error_string):
#         try:
#             template = "An exception of type {0} occurred. Arguments:{1!r}"
#             message = template.format(
#                 type(error_string).__name__, error_string.args)
#             return message
#             # return
#         except Exception as error_string:
#             return error_string



























# -*- coding: UTF-8 -*-
from rolepermissions.roles import AbstractUserRole


class TeacherRole(AbstractUserRole):
    available_permissions = {
        'edit_course': True,
    }


class StudentRole(AbstractUserRole):
    available_permissions = {
        'join_course': True,
    }

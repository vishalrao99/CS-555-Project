from datetime import datetime, timedelta, date

from dateutil.relativedelta import relativedelta

import ReportUtils
from Family import Family
from Individual import Individual

individual_list = []
family_list = []


def get_family_by_family_id(family_id):
    for family in family_list:
        if family.get_id() == family_id:
            return family


def get_indiv_by_indiv_id(indiv_id):
    for indiv in individual_list:
        if indiv.get_id() == indiv_id:
            return indiv


def us01_dates_before_current_date(date, date_type, object_passed):
    if not date < datetime.now():
        if type(object_passed) is Individual:
            ReportUtils.add_error_found("Error US01: " + str(date_type) + " of " + object_passed.get_full_name() + " (" + str(object_passed.id) + ") occurs before current date.")

        if type(object_passed) is Family:
            ReportUtils.add_error_found("Error US01: " + str(date_type) + " of Family (" + str(object_passed.id) + ") occurs before current date.")

        return False
    else:
        return True


def us02_birth_before_marriage(birth_date, marriage_date, indiv_name, indiv_id, family_id):
    if birth_date > marriage_date:
        ReportUtils.add_error_found("Error US02: Birth date of " + str(indiv_name) + " (" + str(indiv_id) + ") occurs before marriage date. (" + str(family_id) + ")")
        return True
    else:
        return False


def us03_birth_before_death(birth_date, death_date, indiv_name, indiv_id):
    if birth_date > death_date:
        ReportUtils.add_error_found("Error US03: Death date of " + str(indiv_name) + " (" + str(indiv_id) + ") occurs before birth date.")
        return False
    else:
        return True


def us04_marriage_before_divorce(marriage_date, divorce_date, indiv_name, indiv_id, family_id):
    if marriage_date > divorce_date:
        ReportUtils.add_error_found("Error US04: Divorce date of " + str(indiv_name) + " (" + str(indiv_id) + ") occurs before marriage date. (" + str(family_id) + ")")
        return False
    else:
        return True


def us05_marriage_before_death(marriage_date, death_date, indiv_name, indiv_id, family_id):
    if marriage_date > death_date:
        ReportUtils.add_error_found("Error US05: Marriage date of " + str(indiv_name) + " (" + str(indiv_id) + ") occurs before death date. (" + str(family_id) + ")")
        return False
    else:
        return True


def us06_divorce_before_death(divorce_date, death_date, indiv_name, indiv_id, family_id):
    if divorce_date > death_date:
        ReportUtils.add_error_found("Error US06: Divorce date of " + str(indiv_name) + " (" + str(indiv_id) + ") occurs before death date. (" + str(family_id) + ")")
        return False
    else:
        return True


def us07_age_less_than_150(birth_date, death_date, indiv_name, indiv_id) -> bool:
    current_date: datetime = datetime.now()
    years_150 = timedelta(days=54750)

    if death_date:
        if birth_date - death_date > timedelta(days=0): 
            ReportUtils.add_error_found("Error US07: Age of " + str(indiv_name) + " (" + str(indiv_id) + ") is Greater than 150 years.")
            return False
        elif death_date - birth_date < years_150: 
            return True
    else:
        if current_date - birth_date < years_150: return True
    ReportUtils.add_error_found("Error US07: Age of " + str(indiv_name) + " (" + str(indiv_id) + ") is not Greater than 150 years.")
            
    return False


def us08_birth_before_marriage_of_parents(birth_date, marriage_date, divorce_date, indiv_name, indiv_id, family_id) -> bool:
    
    if marriage_date:
        if birth_date - marriage_date > timedelta(minutes=0) and birth_date - divorce_date < timedelta(days=275):
            return True
        else:
            ReportUtils.add_error_found("Error US08:  "+ str(indiv_name) +  " (" + str(indiv_id) + ") has not birth before the marriage of Parents. (" + str(family_id) + ")")
            return False
    else:
        ReportUtils.add_error_found("Error US08:  "+ str(indiv_name) +  " (" + str(indiv_id) + ") Parents did not done Marriage. (" + str(family_id) + ")")

def us11_no_bigamy(family_id)->bool:
    for f in family_id:
        if 'HUSB' in family_id[f]:
            hus_id = family_id[f]['HUSB']
            if 'WIFE' in family_id[f]:
                wife_id = family_id[f]['WIFE']

        wife_count = 0
        husb_count = 0

        for f in family_id:
            if 'HUSB' in family_id[f]:
                hus_id2 = family_id[f]['HUSB']
                if hus_id == hus_id2:
                    husb_count += 1
                    if husb_count > 1 :
                     ReportUtils.add_error_found("Error US11: Husband performing bigamy")
                     return False
                if 'WIFE' in family_id[f]:
                    wife_id2 = family_id[f]['WIFE']
                    if wife_id == wife_id2:
                        wife_count += 1
                        if wife_count > 1 :
                         ReportUtils.add_error_found("Error US11: Wife performing bigamy")
                         return False
            else:
                return True

def us12_parents_not_too_old(motherAge,fatherAge,chilAge,indiv_name, indiv_id, family_id):

    motherAge = indiv_id(family_id['WIFE'])['age']
    fatherAge = indiv_id(family_id['HUSB'])['age']
    chilAge  = family_id['CHIL']
    if motherAge - chilAge > 60 :
        ReportUtils.add_error_found("Error US05: Mother is too old for  "+ str(indiv_name) +  " (" + str(indiv_id) + "). (" + str(family_id) + ")")
        return False
    elif fatherAge - chilAge > 80:
        ReportUtils.add_error_found("Error US05: Father is too old for  "+ str(indiv_name) +  " (" + str(indiv_id) + "). (" + str(family_id) + ")")
        return False
    else:
        return True

def us09_birth_before_death_of_parents(birth_date, mother_death_date, father_death_date, indiv_name, indiv_id, family_id):
    is_birth_date_before_mother_death = True if mother_death_date is not None and mother_death_date < birth_date else False
    is_birth_date_before_father_death = True if father_death_date is not None and father_death_date < birth_date + relativedelta(months=-9) else False

    if is_birth_date_before_father_death and is_birth_date_before_mother_death:
        ReportUtils.add_error_found("Error US09: Birth of " + str(indiv_name) + "(" + str(indiv_id) + ")" + " occurs after death of mother and after 9 months after death of father. (" + str(family_id) + ")")
        return True
    elif is_birth_date_before_mother_death:
        ReportUtils.add_error_found("Error US09: Birth of " + str(indiv_name) + "(" + str(indiv_id) + ")" + " occurs after death of mother. (" + str(family_id) + ")")
        return True
    elif is_birth_date_before_father_death:
        ReportUtils.add_error_found("Error US09: Birth of " + str(indiv_name) + "(" + str(indiv_id) + ")" + " occurs after 9 months after death of father. (" + str(family_id) + ")")
        return True

    return False


def us10_marriage_after_14(marriage_date, wife_birth_date, husband_birth_date, family_id):
    if marriage_date is not None:
        is_wife_marriage_after_14 = True if wife_birth_date is not None and wife_birth_date + relativedelta(years=+14) > marriage_date else False
        is_husb_marriage_after_14 = True if husband_birth_date is not None and husband_birth_date + relativedelta(years=+14) > marriage_date else False

        if is_husb_marriage_after_14 and is_wife_marriage_after_14:
            ReportUtils.add_error_found("Error US10: Marriage occurs before both spouses are at least 14 years old. (" + str(family_id) + ")")
            return True
        elif is_wife_marriage_after_14:
            ReportUtils.add_error_found("Error US10: Marriage occurs before wife is at least 14 years old. (" + str(family_id) + ")")
            return True
        elif is_husb_marriage_after_14:
            ReportUtils.add_error_found("Error US10: Marriage occurs before husband is at least 14 years old. (" + str(family_id) + ")")
            return True

    return False

def us15_fewer_than_15_siblings(family) -> bool:
  if len(family.children) < 15:
      print("Success: Family (" + family.id +  ") : Siblings are less than 15")
      return True
  else:
      print("Error US15: Family (" + family.id + ") : Siblings are greater than 15")
      return False

def us16_male_last_names(husb, wife, child, individuals):
    ids = [husb, wife]
    ids.extend(child)
    males = [individual for individual in individuals if individual.gender == 'M' and individual.id in ids]
    names = [male.name.split('/')[1] for male in males]
    if len(set(names)) == 1:
        return True
    else:
        print("Error US16: This Male has differnet last name or has no last Name.")
        return False

def is_indiv_valid(indiv):
    is_valid = True

    if indiv.name is None:
        is_valid = False
        indiv_name = str('Person with ID ' + indiv.id)
        ReportUtils.add_error_found("Error: " + indiv_name + " cannot have empty name.")
    else:
        indiv_name = indiv.get_full_name()

    if indiv.birth_date is None:
        is_valid = False
        ReportUtils.add_null_error_for_indiv(indiv_name, "Birth date")

    return is_valid


def is_fam_valid(fam):
    is_valid = True

    if fam.marriage_date is None:
        is_valid = False
        ReportUtils.add_null_error_for_fam(fam.id, "Marriage date")

    if fam.husb is None:
        is_valid = False
        ReportUtils.add_null_error_for_fam(fam.id, "Husband Id")

    if fam.wife is None:
        is_valid = False
        ReportUtils.add_null_error_for_fam(fam.id, "Wife Id")

    return is_valid


def validate_data(individuals, families):
    global individual_list
    individual_list = individuals

    global family_list
    family_list = families

    for indiv in individual_list:
        if is_indiv_valid(indiv):
            us01_dates_before_current_date(indiv.birth_date, 'Birth date', indiv)

            if indiv.death_date is not None:
                us01_dates_before_current_date(indiv.death_date, 'Death date', indiv)
                us03_birth_before_death(indiv.birth_date, indiv.death_date, indiv.get_full_name(), str(indiv.id))
                us07_age_less_than_150(indiv.birth_date, indiv.death_date, indiv.get_full_name(), str(indiv.id))

            if indiv.get_family_id_as_spouse() != 'NA':
                for family_id in indiv.family_id_as_spouse:
                    family_data = get_family_by_family_id(family_id)

                    if family_data is not None and family_data.marriage_date is not None:
                        us02_birth_before_marriage(indiv.birth_date, family_data.marriage_date, indiv.get_full_name(), str(indiv.id), str(family_id))

                        if family_data.divorce_date is not None:
                            us08_birth_before_marriage_of_parents(indiv.birth_date, family_data.marriage_date,
                                                                  family_data.divorce_date, indiv.get_full_name(),
                                                                  str(indiv.id), str(family_id))
                            us04_marriage_before_divorce(family_data.marriage_date, family_data.divorce_date, indiv.get_full_name(), str(indiv.id), str(family_id))
                            if indiv.death_date is not None:
                                us06_divorce_before_death(family_data.divorce_date, indiv.death_date,
                                                          indiv.get_full_name(), str(indiv.id), str(family_id))

                        if indiv.death_date is not None:
                            us05_marriage_before_death(family_data.marriage_date, indiv.death_date, indiv.get_full_name(), str(indiv.id), str(family_id))

    for family in family_list:
        if is_fam_valid(family):
            father_info = get_indiv_by_indiv_id(family.husb)
            mother_info = get_indiv_by_indiv_id(family.wife)

            us01_dates_before_current_date(family.marriage_date, 'Marriage date', family)
            us10_marriage_after_14(family.marriage_date, mother_info.birth_date, father_info.birth_date, family.id)

            if family.get_children() != 'NA':
                for child in family.children:
                    child_info = get_indiv_by_indiv_id(child)

                    us09_birth_before_death_of_parents(child_info.birth_date, mother_info.death_date, father_info.death_date, child_info.get_full_name(), child_info.id, family.id)

            if family.divorce_date is not None:
                us01_dates_before_current_date(family.divorce_date, 'Divorce date', family)

            if indiv.get_family_id_as_spouse() != 'NA':
                for family_id in indiv.family_id_as_spouse:
                    family_data = get_family_by_family_id(family_id)


    ReportUtils.compile_report()

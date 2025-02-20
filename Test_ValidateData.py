import unittest

from Family import Family
from Individual import Individual


from ValidateData import us01_dates_before_current_date, us02_birth_before_marriage, us03_birth_before_death,us04_marriage_before_divorce,us07_age_less_than_150, us08_birth_before_marriage_of_parents,us05_marriage_before_death, us06_divorce_before_death, us15_fewer_than_15_siblings, us16_male_last_names, us09_birth_before_death_of_parents, us10_marriage_after_14,us11_no_bigamy,us12_parents_not_too_old




class TestValidateDataMethod(unittest.TestCase):
    def setUp(self):
        self.individual = Individual("Indiv1")
        self.individual.set_name("Individual /1/")
        self.individual.set_birth_date("12 DEC 1968")
        self.individual.set_death_date("18 JAN 2021")
        self.individual.set_family_id_as_spouse("Fam1")

        self.individual2 = Individual("Indiv2")
        self.individual.set_name("Individual /2/")
        self.individual2.set_birth_date("1 APR 1968")
        self.individual2.set_death_date("13 AUG 2021")
        self.individual2.set_family_id_as_spouse("Fam1")

        self.individual3 = Individual("Indiv3")
        self.individual.set_name("Individual /3/")
        self.individual3.set_birth_date("13 AUG 2021")
        self.individual3.set_family_id_as_child("Fam1")

        self.family = Family("Fam1")
        self.family.set_husb("Indiv1")
        self.family.set_wife("Indiv2")
        self.family.set_children("Indiv3")
        self.family.set_marriage_date("5 DEC 2001")
        self.family.set_divorce_date("10 JUL 2011")

    def tearDown(self):
        del self.family
        del self.individual

    def test_us01_dates_before_current_date(self):
        self.assertTrue(us01_dates_before_current_date(self.individual.birth_date, "Birth date", self.individual))
        self.assertTrue(us01_dates_before_current_date(self.individual.death_date, "Death date", self.individual))
        self.assertTrue(us01_dates_before_current_date(self.family.marriage_date, "Marriage date", self.family))
        self.assertTrue(us01_dates_before_current_date(self.family.divorce_date, "Divorce date", self.family))

        self.individual.set_birth_date("12 DEC 2068")
        self.assertFalse(us01_dates_before_current_date(self.individual.birth_date, "Birth date", self.individual))

        self.individual.set_death_date("18 JAN 2050")
        self.assertFalse(us01_dates_before_current_date(self.individual.death_date, "Death date", self.individual))

        self.family.set_marriage_date("5 DEC 2060")
        self.assertFalse(us01_dates_before_current_date(self.family.marriage_date, "Marriage date", self.family))

        self.family.set_divorce_date("10 JUL 2065")
        self.assertFalse(us01_dates_before_current_date(self.family.divorce_date, "Divorce date", self.family))

    def test_us02_birth_before_marriage(self):
        self.assertFalse(us02_birth_before_marriage(self.individual.birth_date, self.family.marriage_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.individual.set_birth_date("12 DEC 2068")
        self.assertTrue(us02_birth_before_marriage(self.individual.birth_date, self.family.marriage_date, self.individual.get_full_name(), self.individual.id, self.family.id))
    
    def test_us05_marriage_before_death(self):
        self.assertTrue(us05_marriage_before_death(self.family.marriage_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.family.set_marriage_date("05 Jan 1999")
        self.individual.set_death_date("21 Mar 1860")
        self.assertFalse(us05_marriage_before_death(self.family.marriage_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.family.set_marriage_date("05 Jan 1992")
        self.individual.set_death_date("21 Mar 2060")
        self.assertTrue(us05_marriage_before_death(self.family.marriage_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.family.set_marriage_date("05 Jan 2020")
        self.individual.set_death_date("21 Mar 1960")
        self.assertFalse(us05_marriage_before_death(self.family.marriage_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id, self.family.id))

    def test_us06_divorce_before_death(self):
        self.assertTrue(us06_divorce_before_death(self.family.divorce_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.family.set_divorce_date("11 Jan 2021")
        self.individual.set_death_date("15 Jun 2007")
        self.assertFalse(us06_divorce_before_death(self.family.divorce_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.family.set_divorce_date("11 Mar 2000")
        self.individual.set_death_date("15 Jun 2019")
        self.assertTrue(us06_divorce_before_death(self.family.divorce_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.family.set_divorce_date("11 Mar 2012")
        self.individual.set_death_date("15 Jun 2001")
        self.assertFalse(us06_divorce_before_death(self.family.divorce_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id, self.family.id))

    def test_us03_birth_before_death(self):
        self.assertTrue(us03_birth_before_death(self.individual.birth_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id))

        self.individual.set_birth_date("05 Jan 2000")
        self.individual.set_death_date("21 Mar 1760")
        self.assertFalse(us03_birth_before_death(self.individual.birth_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id))

        self.individual.set_birth_date("05 Jan 1997")
        self.individual.set_death_date("21 Mar 2050")
        self.assertTrue(us03_birth_before_death(self.individual.birth_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id))

        self.individual.set_birth_date("05 Jan 2056")
        self.individual.set_death_date("21 Mar 1960")
        self.assertFalse(us03_birth_before_death(self.individual.birth_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id))

    def test_us04_marriage_before_divorce(self):
        self.assertTrue(us04_marriage_before_divorce(self.family.marriage_date, self.family.divorce_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.individual.set_birth_date("14 Jun 1997")
        self.family.set_marriage_date("11 Mar 2021")
        self.family.set_divorce_date("15 Jun 2010")
        self.assertFalse(us04_marriage_before_divorce(self.family.marriage_date, self.family.divorce_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.individual.set_birth_date("17 Oct 1960")
        self.family.set_marriage_date("11 Mar 2004")
        self.family.set_divorce_date("15 Jun 2010")
        self.assertTrue(us04_marriage_before_divorce(self.family.marriage_date, self.family.divorce_date, self.individual.get_full_name(), self.individual.id, self.family.id))

        self.individual.set_birth_date("11 Jun 1964")
        self.family.set_marriage_date("11 Mar 2016")
        self.family.set_divorce_date("15 Jun 2010")
        self.assertFalse(us04_marriage_before_divorce(self.family.marriage_date, self.family.divorce_date, self.individual.get_full_name(), self.individual.id, self.family.id))

    def test_us07_age_less_than_150(self):
        self.assertTrue(us07_age_less_than_150(self.individual.birth_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id))
        
        self.individual.set_birth_date("15 Feb 2012")
        self.individual.set_death_date("21 Jan 2000")
        
        self.assertFalse(us07_age_less_than_150(self.individual.birth_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id))
        
        self.individual.set_birth_date("05 Jan 1960")
        self.individual.set_death_date("21 Mar 2000")
        
        self.assertTrue(us07_age_less_than_150(self.individual.birth_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id))
        
        self.individual.set_birth_date("25 SEP 1760")
        self.individual.set_death_date("11 Jan 2000")
        
        self.assertFalse(us07_age_less_than_150(self.individual.birth_date, self.individual.death_date, self.individual.get_full_name(), self.individual.id))
    
    def test_us08_birth_before_marriage_of_parents(self):
        self.individual.set_birth_date("15 Feb 2008")
        
        self.assertTrue(us08_birth_before_marriage_of_parents(self.individual.birth_date, self.family.marriage_date, self.family.divorce_date, self.individual.get_full_name(), self.individual.id, self.family.id))
        
        self.individual.set_birth_date("15 Feb 2008")
        self.family.set_marriage_date("11 Mar 2004")
        self.family.set_divorce_date("15 Jun 2010")
        
        self.assertTrue(us08_birth_before_marriage_of_parents(self.individual.birth_date, self.family.marriage_date, self.family.divorce_date, self.individual.get_full_name(), self.individual.id, self.family.id))
        
        self.individual.set_birth_date("25 Jan 2015")
        self.family.set_marriage_date("01 Sep 2004")
        self.family.set_divorce_date("15 Jun 2010")
        

        self.assertFalse(us08_birth_before_marriage_of_parents(self.individual.birth_date, self.family.marriage_date, self.family.divorce_date, self.individual.get_full_name(), self.individual.id, self.family.id))   
        

    def test_us09_birth_before_death_of_parents(self):
        # parents death occur after birth
        self.assertFalse(us09_birth_before_death_of_parents(self.individual3.birth_date, self.individual2.death_date, self.individual.death_date, self.individual3.get_full_name(), self.individual3.get_id(), self.family.id))

        # both parents death occur before birth
        self.individual.set_death_date("11 JAN 2020")
        self.individual2.set_death_date("10 AUG 2021")
        self.assertTrue(us09_birth_before_death_of_parents(self.individual3.birth_date, self.individual2.death_date, self.individual.death_date, self.individual3.get_full_name(), self.individual3.get_id(), self.family.id))

        # mother death occur before birth
        self.individual.set_death_date("18 JAN 2021")
        self.assertTrue(us09_birth_before_death_of_parents(self.individual3.birth_date, self.individual2.death_date, self.individual.death_date, self.individual3.get_full_name(), self.individual3.get_id(), self.family.id))

        # father death occur before birth
        self.individual.set_death_date("11 JAN 2020")
        self.individual2.set_death_date("13 AUG 2021")
        self.assertTrue(us09_birth_before_death_of_parents(self.individual3.birth_date, self.individual2.death_date, self.individual.death_date, self.individual3.get_full_name(), self.individual3.get_id(), self.family.id))

        self.assertFalse(us09_birth_before_death_of_parents(None, None, None, None, None, None))

    def test_us10_marriage_after_14(self):
        # both spouses were over 14 when marriage happened
        self.assertFalse(us10_marriage_after_14(self.family.marriage_date, self.individual2.birth_date, self.individual.birth_date, self.family.id))

        # both spouses were under 14 when marriage happened
        self.individual2.set_birth_date("1 APR 2020")
        self.individual.set_birth_date("12 DEC 2019")
        self.assertTrue(us10_marriage_after_14(self.family.marriage_date, self.individual2.birth_date, self.individual.birth_date, self.family.id))

        # wife was under 14 when marriage happened
        self.individual.set_birth_date("12 DEC 1968")
        self.assertTrue(us10_marriage_after_14(self.family.marriage_date, self.individual2.birth_date, self.individual.birth_date, self.family.id))

        # husband was under 14 when marriage happened
        self.individual.set_birth_date("12 DEC 2020")
        self.individual2.set_birth_date("1 APR 1968")
        self.assertTrue(us10_marriage_after_14(self.family.marriage_date, self.individual2.birth_date, self.individual.birth_date, self.family.id))

        self.assertFalse(us10_marriage_after_14(None, None, None, self.family.id))
        self.assertFalse(us10_marriage_after_14(self.family.marriage_date, None, None, self.family.id))

    def test_us15_fewer_than_15_siblings(self):
        self.family.set_husb("I0")
        self.family.set_wife("I1")
        self.family.set_children("I2")
        self.family.set_children("I3")
        self.family.set_children("I4")
        self.family.set_children("I5")
        self.family.set_children("I6")
        self.family.set_children("I7")
        self.family.set_children("I8")
        self.family.set_children("I9")
        self.family.set_children("I10")
        self.family.set_children("I11")
        self.family.set_children("I12")
        self.family.set_children("I13")
        self.family.set_children("I14")
        self.family.set_children("I15")
        self.family.set_children("I16")
        self.family.set_children("I17")
        self.assertFalse(us15_fewer_than_15_siblings(self.family))
        
        self.family.children = []
        self.family.set_children("I2")
        self.family.set_children("I3")
        self.family.set_children("I4")
        self.family.set_children("I5")
        self.family.set_children("I6")
        self.family.set_children("I7")
        self.family.set_children("I8")
        self.assertTrue(us15_fewer_than_15_siblings(self.family))
        
    def test_us16_male_last_names(self):
        individuals = []
        self.individual = Individual("Indv0")
        self.individual.set_name("Pablo /Escobar/")
        self.individual.set_gender('M')
        self.family.set_husb("Indv0")
        individuals.append(self.individual)
        self.individual = Individual("Indv1")
        self.individual.set_name("Veronika /Esco/")
        self.individual.set_gender('F')
        self.family.set_wife("Indv1")
        individuals.append(self.individual)
        self.individual = Individual("Indv2")
        self.individual.set_name("Terry /Escobart/")
        self.individual.set_gender('M')
        self.family.set_children("Indv2")
        individuals.append(self.individual)
        self.individual = Individual("Indv3")
        self.individual.set_name("Maria /Escobar/")
        self.individual.set_gender('F')
        self.family.set_children("Indv3")
        individuals.append(self.individual)
        self.assertFalse(us16_male_last_names(self.family.husb, self.family.wife, self.family.children, individuals))
        
        individuals = []
        self.individual = Individual("Indv0")
        self.individual.set_name("Danis /Hazard/")
        self.individual.set_gender('M')
        self.family.set_husb("Indv0")
        individuals.append(self.individual)
        self.individual = Individual("Indv1")
        self.individual.set_name("Vina /Hazard/")
        self.individual.set_gender('F')
        self.family.set_wife("Indv1")
        individuals.append(self.individual)
        self.individual = Individual("Indv2")
        self.individual.set_name("JR /Hazard/")
        self.individual.set_gender('M')
        self.family.set_children("Indv2")
        individuals.append(self.individual)
        self.individual = Individual("Indv3")
        self.individual.set_name("SR /Hazard/")
        self.individual.set_gender('M')
        self.family.set_children("Indv3")
        individuals.append(self.individual)
        self.assertTrue(us16_male_last_names(self.family.husb, self.family.wife, self.family.children, individuals))

        individuals = []
        self.individual = Individual("Indv0")
        self.individual.set_name("Nick /Walter/")
        self.individual.set_gender('M')
        self.family.set_husb("Indv0")
        individuals.append(self.individual)
        self.individual = Individual("Indv1")
        self.individual.set_name("Moni /Walter/")
        self.individual.set_gender('F')
        self.family.set_wife("Indv1")
        individuals.append(self.individual)
        self.individual = Individual("Indv2")
        self.individual.set_name("Maris /Walter/")
        self.individual.set_gender('M')
        self.family.set_children("Indv2")
        individuals.append(self.individual)
        self.individual = Individual("Indv3")
        self.individual.set_name("Haly /Walters/")
        self.individual.set_gender('M')
        self.family.set_children("Indv3")
        individuals.append(self.individual)
        self.assertFalse(us16_male_last_names(self.family.husb, self.family.wife, self.family.children, individuals))

        
 def test_us11_no_bigamy(self):
        self.assertTrue(us11_no_bigamy(self.family))
      
        self.assertFalse(us11_no_bigamy(self.family))

    def test_us12_parents_not_too_old(self):

        husb_age= self.individual.set_age("18 Sep 1960")
        wife_age = self.individual.set_age("18 Dec 1964")
        child_age= self.individual.set_age("20 Apr 2000")
        self.assertTrue(us12_parents_not_too_old(husb_age,wife_age,child_age, self.individual.get_full_name(),self.individual.id, self.family.id))

        
        husb_age= self.individual.set_age("23 Jun 1920")
        wife_age = self.individual.set_age("14 Apr 1924")
        child_age= self.individual.set_age("11 Jul 2010")
        self.assertFalse(us12_parents_not_too_old(husb_age,wife_age,child_age, self.individual.get_full_name(),self.individual.id, self.family.id))
    
if __name__ == "__main__":
    unittest.main(exit=False)

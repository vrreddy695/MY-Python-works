class Employee:
    raise_amount=1.04
    def __init__(self, fname, lname, pay):
        self.fname=fname
        self.lname=lname
        self.pay=pay
        self.email=fname+'.'+lname+'@gmail.com'
    def fullname(self):
        return '{} {}'.format(self.fname, self.lname)
    def apply_raise(self):
        self.pay=int(self.pay * self.raise_amount)
        
    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amount=amount
    @staticmethod
    def is_workday(day):
        if day.weekday()==5 or day.weekday()==6:
            return False
        return True
class Developer(Employee):
    raise_amount=1.10
    def __init__(self, fname, lname, pay, prog_lang):
        self.prog_lang=prog_lang
        Employee.__init__(self,fname, lname, pay)
                
    
    
emp1=Developer('vrreddy', 'koppula', 50000, 'python')
emp2=Developer('Narsireddy', 'koppula', 50000,'java')
#emp1=Employee('vrreddy', 'koppula', 50000)
#Employee.set_raise_amt(1.06)
# print 'Raise amount: %s' %emp1.raise_amount
# print 'Employee fullname: %s' %emp1.fullname()
# print 'Employeee pay: %s' %emp1.pay
# import datetime
# my_date=datetime.date(2016,8,10)
# print 'Is work day: %s' %emp1.is_workday(my_date)
# print help(Developer)
#emp1.apply_raise()
print emp1.prog_lang
print emp2.prog_lang
print emp1

 

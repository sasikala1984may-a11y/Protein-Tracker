import mysql.connector
con_obj=mysql.connector.connect(host='localhost',username='root',passwd='ridhan',database='protien_tracker')
if con_obj.is_connected():
    print('successfully connected')
cur_obj=con_obj.cursor()
def add_meal():  
    ans='yes'
    while ans=="yes" or ans=='Yes':
        print("\t\t-----ADDING PROTEIN CONTENT DETAILS-----")
        meal=input("Enter a food :")
        pr=float(input("Enter the protein quantity (per 100g) in '{}':".format(meal)))
        cur_obj.execute('''insert into pro_content
        values('{}',{})'''.format(meal,pr))
        con_obj.commit()
        print("SUCCESSFULLY ADDED")
        ans=input("Do u want to add another food and its protein content ??(yes/No): ")
                                     
def show_meal():
    print("\t\t-----DISPLAYING PROTEIN CONTENT IN ALL THE FOODS-----")
    cur_obj.execute("select* from pro_content")
    data=cur_obj.fetchall()
    print("( FOOD , PROTEIN(/100gms))")
    for i in data:
        print(i)

def pro_calc():
    sum=0
    print("\t\t-----DAILY PROTEIN INTAKE CALCULATOR-----")
    n=int(input("Enter how many variety of food ate today :"))

    for i in range(n):
        food=input("Enter the food :")
        cur_obj.execute("select * from pro_content")
        dt=cur_obj.fetchall()
        found=False
        for j in dt:
            if j[0].lower()==food.lower():
                found=True
                if food.lower()=='egg':
                    qty1=int(input("Enter how much egg ate:"))
                    sum=sum+((j[1])*float(qty1))
                else:
                    qty=int(input("Enter quantity (gms) :"))
                    per_gram=j[1]/100
                    tot_intake=qty*per_gram
                    sum+=tot_intake
                break
        if found==False:
            print("Food item not found")
            ans=input("Enter do you want to add food to database (yes/no):")
            if ans=='yes' or ans=='Yes':
                add_meal()
                cur_obj.execute("select * from pro_content")
                dt=cur_obj.fetchall()
                for j in dt:
                    if j[0].lower()==food.lower():
                        print("\t\t-----Food added successfully-----")
                        qty=int(input("Enter quantity (gms) :"))
                        per_gram=j[1]/100
                        tot_intake=qty*per_gram
                        sum+=tot_intake
                        break
            else:
                print("Exit")

    print("Good you have totally added", sum, "gms of protein to your diet")


def delete_meal():
    print("\t\t-----DELETING FOOD FROM DATABASE-----")
    ans='yes'
    while ans.lower()=='yes':
        fd=input("Enter the food which you want to delete :")
        cur_obj.execute('''Delete from pro_content
                    where Food='{}' '''.format(fd))
        con_obj.commit()
        print("SUCCESSFULLY DELETED")
        ans=input("Do you want to delete another food (yes/no) :")

def update():
    print("\t\t-----UPDATING DATABASE-----")
    ans='yes'
    while ans.lower()=='yes':
        fd=input("Enter food for which u have to update protein content:")
        nv=float(input("Enter the new value(per 100gms):"))
        cur_obj.execute('''update pro_content
                        set Protien_content={}
                        where Food='{}' '''.format(nv,fd))
        print("SUCCESSFULLY UPDATED")
        ans=input("Do you want to update another food protein content ? (yes/no) :")

print("*"*75)
print("\t\t\t   PROTEIN TRACKER   \t\t\t")
print("*"*75)
ans='yes'
while ans.lower()=='yes':
    ch=int(input('''\n\nENTER
             1. Add food and protein content
             2. Display all the food and protein content
             3. Daily protein tracker
             4. Delete a food
             5. Update the protein value of a food
             6. Exit
             (1/2/3/4/5/6) :: '''))
    if ch==1:
        add_meal()
    elif ch==2:
        show_meal()
    elif ch==3:
        pro_calc()
    elif ch==4:
        delete_meal()
    elif ch==5:
        update()
    else:
        ans='no'
        print("*"*75)
        print("\n\t\t\t THANK YOU  \t\t\n")
        print("*"*75)

             
    

    
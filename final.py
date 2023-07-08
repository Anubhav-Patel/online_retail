import mysql.connector
import datetime;
conn=mysql.connector.connect(host='localhost',username='root',password='mysql@pass#123',database='onestopshop')

sqlcursor=conn.cursor()

del_id=302
def maxIdInTable(id_name,table_name):
    sqlcursor.execute(f"SELECT {id_name} FROM {table_name} ;")
    ans2=sqlcursor.fetchall()
    id_max=0
    id_final=0
    # print(ans2)
    for i in ans2:
        
        i=list(i)
        i=i[0]
        i=i.replace("'","",2)
       
        id_max=int(i)
        
        id_max+=1
        if(id_max>id_final):
            id_final=id_max
        id_max=str(id_final)
  
    return id_final

n=1
def signup(n):
    if(n==1):
        try:
            print("Enter username: ")
            id=input()
            sqlcursor.execute(f"SELECT user_id FROM customer where name='{id}';")
            ans=sqlcursor.fetchall()
            if(len(ans)):
                print("username already exist")
            else:
                print("Enter password: ")
                pswd=input()
                print("Enter date of birth(yyyy-mm-dd)")    
                dob=input()
                print("Enter house no")    
                house=input()
                print("Enter area ")    
                area=input()
                print("Enter city ")    
                city=input()
                print("Enter state ")    
                state=input()
                print("Enter pincode")    
                pin=input()
                id_final=maxIdInTable("user_id","customer")
                sqlcursor.execute(f"insert into customer (user_id, name, password, dob) values ('{id_final}','{id}', '{pswd}', '{dob}');")
                sqlcursor.execute(f"insert into wallet(user_id,amount) values ('{id_final}','10000')")
                sqlcursor.execute(f"insert into address (id,house_no,area,city,state,pincode) values ('{id_final}','{house}','{area}', '{city}', '{state}','{pin}');")
                print("user is registered")
                conn.commit()   
        except:
           print("error in input")
            
    if(n==2):
        try:
            print("Enter username: ")
            id=input()
            sqlcursor.execute(f"SELECT seller_id FROM seller where name='{id}';")
            ans=sqlcursor.fetchall()
            if(len(ans)):
                print("username already exist")
            else:
                print("Enter password: ")
                pswd=input()
                print("Enter phone no")    
                phone=input()
                id_final=maxIdInTable("seller_id","seller")
                sqlcursor.execute(f"insert into seller (seller_id, name, password, contact_no) values ('{id_final}','{id}', '{pswd}', '{phone}');")
                conn.commit() 
                print("user is registered")  
        except:
           print("error in input")
    if(n==3):
        try:
            print("Enter username: ")
            id=input()
            sqlcursor.execute(f"SELECT delivery_id FROM delivery where name='{id}';")
            ans=sqlcursor.fetchall()
            if(len(ans)):
                print("username already exist")
            else:
                print("Enter password: ")
                pswd=input()
                print("Enter phone no")    
                phone=input()
                
                id_final=maxIdInTable("seller_id","seller")
                sqlcursor.execute(f"insert into delivery (delivery_id, name, password, contact_no) values ('{id_final}','{id}', '{pswd}', '{phone}');")
                print("user is registered")
                conn.commit()   
        except:
           print("error in input")



def customerCatalog(id):
    print()
    n=1
    while(n!=8):
        print('''1). browse products
2). see cart
3). check wallet
4). add money
5). add to cart
6). checkout
7). purchase history
8). exit''')
        
        print("Enter your choice: ")
        n=int(input())
        if(n==1):
            sqlcursor.execute(f"SELECT * FROM product;")
            ans=sqlcursor.fetchall()
            
            for i in ans:
                i=list(i)
                print("product name: ",i[1])
                print("price: ",i[2])
                print("detail: ",i[4])
                print()

        if(n==2):
            sqlcursor.execute(f"SELECT * FROM cart where user_id='{id}';")
            ans=sqlcursor.fetchall()
            
            for i in ans:
                i=list(i)
                print("product id: ",i[1])
                print("price: ",i[3])
                # print("detail: ",i[4])
                print()
            
        if(n==3):
            sqlcursor.execute(f"SELECT * FROM wallet where user_id='{id}';")
            ans=sqlcursor.fetchall()
            
            for i in ans:
                i=list(i)
                print("wallet amount: ",i[1])
                print()
            
        if(n==4):
            print("Enter money to add: ")
            money=int(input())
            sqlcursor.execute(f"SELECT * FROM wallet where user_id='{id}';")
            ans=sqlcursor.fetchall()
            for i in ans:
                i=list(i)
                money+=int(i[1])
            sqlcursor.execute(f"update wallet set amount={money} where user_id='{id}';")
            ans=sqlcursor.fetchall()
            conn.commit()
            print("money added")

        if(n==5):
            print("Enter product id: ")
            pid=input()
            print("Enter quantity: ")
            quantity=input()
            sqlcursor.execute(f"SELECT * FROM product where product_id='{pid}';")
            ans=sqlcursor.fetchall()
            finalprice=1
            for i in ans:
                i=list(i)
                finalprice=int(i[2])*int(quantity)
            sqlcursor.execute(f"insert into cart (user_id, product_id, total_quantity, total_price) values ('{id}','{pid}', '{quantity}', '{finalprice}');")
            ans=sqlcursor.fetchall()
        if(n==6):
            global del_id
            order_id=maxIdInTable("order_id","orderdetail")
            ct = datetime.datetime.now()
            temp_id=del_id
            sqlcursor.execute(f"insert into orderdetail (order_id, customer_id, delivery_id, time,address) values ('{order_id}','{id}', '{temp_id}', '{ct}','');")
            del_id+=1
            ans=sqlcursor.fetchall()
            sqlcursor.execute(f"SELECT * FROM cart where user_id='{id}';")
            ans=sqlcursor.fetchall()
            cart_money=0
            for i in ans:
                i=list(i)
                cart_money=int(i[3])
            sqlcursor.execute(f"delete FROM cart where user_id='{id}';")
            ans=sqlcursor.fetchall()
            sqlcursor.execute(f"SELECT * FROM wallet where user_id='{id}';")
            ans=sqlcursor.fetchall()
            money=0
            for i in ans:
                i=list(i)
                money=int(i[1])-cart_money
            sqlcursor.execute(f"update wallet set amount={money} where user_id='{id}';")
            ans=sqlcursor.fetchall()
            conn.commit()

            
                        
        if(n==7):
            sqlcursor.execute(f"SELECT * FROM orderdetail where customer_id='{id}';")
            ans=sqlcursor.fetchall()
            
            for i in ans:
                i=list(i)
                print("delivery id: ",i[2])
                print("time: ",i[3])
                # print("detail: ",i[4])
                print()
        if(n==8):
            return
def sellerCatalog(id):
    print()
    n=1
    while(n!=3):
        print('''1). add product
2). see products
3). exit''')
        print("Enter your choice: ")
        n=int(input())
        if(n==1):
            try:
                print("Enter name: ")
                name_p=input()
                
                print("Enter price: ")
                price=input()
                print("Enter quantity: ")    
                qun=input()
                print("Enter detail: ")
                detail=input()
                id_final=maxIdInTable("product_id","product")
                sqlcursor.execute(f"insert into product(product_id, name, price, quantity, details,seller_id) values ('{id_final}','{name_p}','{price}', '{qun}', '{detail}','{id}');")
                conn.commit()
                print("product added")   
            except:
               print("error in input")
        if(n==2):
            sqlcursor.execute(f"SELECT * FROM product where seller_id='{id}';")
            ans=sqlcursor.fetchall()
            for i in ans:
                print(i)
                
        if(n==3):
            return
        

def deliveryCatalog(id):
    while(True):
        print('''1). see delivery
2). remove delivery
3). exit''')
        n=int(input())
        if(n==1):
            sqlcursor.execute(f"SELECT * FROM orderdetail where delivery_id='{id}';")
            ans=sqlcursor.fetchall()
            for i in ans:
                i=list(i)
                print("address: ",i[4])

        if(n==2):
            sqlcursor.execute(f"delete FROM orderdetail where delivery_id='{id}';")
            ans=sqlcursor.fetchall()
            conn.commit()
            print("done")
        if(n==3):
            break

while(n!=7):
    print("************************OneStopShop************************\n")
    print('''1) signup for customer
2) signin as customer
3) signup as seller
4) signin as seller
5) signup delivery
6) signin delivery
7) exit
             ''')
    n=int(input("Enter your choice: "))
    if(n==1):
        signup(1)
    if(n==2):
        print("Enter username: ")
        id=input()
        print("Enter password: ")
        pswd=input()
        sqlcursor.execute(f"SELECT user_id FROM customer where name='{id}' and password='{pswd}';")
        ans=sqlcursor.fetchall()
        if(not len(ans)):
                print("user does not exist")
        else:
            for i in ans:
                i=str(i)
                i=str(i[2:-3])  
                customerCatalog(i)
        
    if(n==3):
        signup(2)
    if(n==4):
        print("Enter username: ")
        id=input()
        print("Enter password: ")
        pswd=input()
        sqlcursor.execute(f"SELECT seller_id FROM seller where name='{id}' and password='{pswd}';")
        ans=sqlcursor.fetchall()
        if(not len(ans)):
                print("username does not exist")
        else:
            for i in ans:
                i=str(i)
                i=str(i[2:-3])  
                sellerCatalog(i)
    if(n==5):
        signup(3)

    if(n==6):
        print("Enter username: ")
        id=input()
        print("Enter password: ")
        pswd=input()
        sqlcursor.execute(f"SELECT delivery_id FROM delivery where name='{id}' and password='{pswd}';")
        ans=sqlcursor.fetchall()
        if(not len(ans)):
                print("username does not exist")
        else:
            for i in ans:
                i=list(i)
                i=i[0]
                i=i.replace("'","",2)  
                deliveryCatalog(i)
    if(n==7):
        break

    

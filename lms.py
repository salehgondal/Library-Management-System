#Create management account which is secured by password and can see books in stcok, can rent, can make returns and can block users

#Create user accounts who can search, loan, return and check charges.

import numpy as np
import pandas as pd
import getpass
import os
import re


# clear screen
clear = lambda: os.system('cls')
clear()

# Welcome message
print('\nWelcome to Saleh Public Library')

data = pd.read_csv('booklist.txt', sep=",",)
data["stock"] = pd.to_numeric(data["stock"])

users = pd.read_csv('users.txt', sep=",")

def quit_app(x):
    if x.lower() == 'q':
        print("Do you really want to quit? y/n")
        y = input()
        if y == 'y':
            print("Quitting...")
            return(True)
        else:
            return(False)
    
    else:
        return(False)

def show_booklist(type,user=None):
    if user is not None:
        print(data)
    elif type == 'all':
        print(data['name'].to_string())
    else:
        print(data.loc[data['stock'] > 0,].reset_index().name.to_string())
        
def create_new_account():
    print('\nPlease enter your email address:', end=" ")
    while True:
        email = input().lower()
        
def login():
    clear()
    while True:
        print('\nPlease enter your email address:', end=" ")
        email = input().lower()
        
        if quit_app(email):
            quit()
        
        print(email)
        
        if not users.email.eq(email).any():
            print("Email Address does not exist! Try Again.")
            continue
        else:
            break
    
    while True:    
        
        pass_entered = getpass.getpass('Password:')
        
        if quit_app(pass_entered):
            quit()
        
        if not users[users['email'] == email].password.eq(pass_entered).any():
            print("\nPassword is Incorrect! Try Again.\n")
            continue
        else:
            break
    
    role = users[users['email']==email].role.to_string(index=False).strip()
    clear()
    return([email,role])
    
def change_password(email):
    while True:
        oldpass = getpass.getpass('Please Enter your current Password:')
        if oldpass == 'b':
            break
        if quit_app(oldpass):
                quit()
            
        if not users[users['email'] == email].password.eq(oldpass).any():
            print("\nPassword is Incorrect! Try Again.\n")
            continue
        else:
            while True:
                newpass = getpass.getpass('Please Enter your new Password:')
                newpass_confirm = getpass.getpass('Please Confirm your new Password:')
                
                if newpass != newpass_confirm:
                    print("\nPasswords do not match! Try Again.\n")
                    continue
                else:
                    users.loc[users.email==email,'password'] = newpass
                    users.to_csv('users.txt', sep=",", header=True,index=None)
                    print("Your password has been updated")
                break
        break

def get_user_booklist(avail_books):
    clear()
    for idx,val in enumerate(avail_books):
        print(idx,val)
    while True:
        to_issue = input("\nPlease select the book[s] from the list above. For multiple books, enter the number followed by a space.\n")
        if to_issue == 'b':
            return(to_issue)
        try:
            to_issue = to_issue.strip()
            #print(to_issue)
            
            to_issue = re.sub(' +', ' ', to_issue).split(" ")
            to_issue = list(map(int, to_issue))
            to_issue = list(set(to_issue))
            #avail_books = data.loc[data['stock'] > 0,].reset_index()
            print("\n")
            if any(i < 0 for i in to_issue):
                print("Invalid Entry")
                continue
            #print(avail_books.iloc[to_issue,1].to_string())
            for idx in to_issue:
                print(avail_books[idx])
            print("\n")
            return(to_issue)
        except:
            print("Invalid Entry")
            continue

def issue_books(book_list,book_nums,user):
    book_names = list()
    for i in book_nums:
        book_names.append(book_list[i]) 
    #print(book_names)
    books_already_issued = users.loc[users.email==user,'books_borrowed'].tolist()
    if str(books_already_issued[0]) != 'nan':
        book_names = book_names + books_already_issued
    book_names = list(filter(None,book_names))
    users.loc[users.email==user,'books_borrowed'] = ";".join(book_names)
    users.to_csv('users.txt', sep=",", header=True,index=None)
    
    for book in book_names:
        data.loc[data.name == book,'stock'] = data.loc[data.name == book,'stock'] - 1
    
    data.to_csv('booklist.txt', sep=",", header=True,index=None)

def get_issued_books(user):
    if len(list(filter(None,users.loc[users.email==user,'books_borrowed']))) == 0:
        raise ValueError('A very specific bad thing happened.')
    books_of_user = users.loc[users.email==user,'books_borrowed'].tolist()
    books_of_user = ''.join(books_of_user)
    
    books_of_user = books_of_user.split(";")
    books_of_user = list(filter(None,books_of_user))
    return(books_of_user)

def return_books(books_of_user,return_book_index,user):
    
    return_book_index = list(map(int, return_book_index))
    #print(return_book_index)
    return_book_name = list()
    for i in return_book_index:
        return_book_name.append(books_of_user[i]) 
    
    #print("\n",return_book_name,"\n")
    user_books = users.loc[users.email==user,'books_borrowed'].tolist()
    #print(user_books)
    user_books = user_books[0].split(";")
    for name in return_book_name:
        user_books.remove(name)
    users.loc[users.email==user,'books_borrowed'] = ";".join(user_books)
    users.to_csv('users.txt', sep=",", header=True,index=None)
    for name in return_book_name:
        data.loc[data.name == name,'stock'] = data.loc[data.name == name,'stock'] + 1
    data.to_csv('booklist.txt', sep=",", header=True,index=None)

# main body

x = 0

while True:
    if x not in [0,'2','3','4']:
        clear()
    print('\nPlease choose any option to continue. Enter q to exit.')
    print('\n [1] login    [2] Create new Account    [3] See All books    [4] See Available books')
    x = input()
    
    if quit_app(x):
        quit()
    
    if x not in ['1','2','3','4']:
        print('Invalid Selection. Please Try Again')
        continue
    
    if x == '3':
        show_booklist('all')
        continue
    
    if x == '4':
        show_booklist('instock')
        continue
    
    if x == '1': # login
    
        [user,role] = login()

        if role == 'user':
            if users[(users["email"]==user)].blocked.eq(1).any():
                print("\n\nSorry! You have been blocked from the Library. Please see the Librarian.\n")
                x = 0
                continue
            while True:
                
                y = input("What would you like to do today?\n[1] Issue a book    [2] Return a book    [3] See books Issued to me    [4] Change Password \n")
                if y == 'b':
                    break
                if quit_app(y):
                    quit()
                
                if y == '1': # issue book
                    books_in_stock = data.loc[data['stock'] > 0,'name'].values.tolist()
                    while True:
                        
                        to_issue = get_user_booklist(books_in_stock)
                        x = input("[y] Confirm  [n] Modify\n")
                        
                        if x.lower() != 'y':
                            continue
                        else:
                            # write function to add books to user
                            issue_books(books_in_stock,to_issue,user)
                            clear()
                            break
                
                if y == '2': # return a book
                    try:
                        books_of_user = get_issued_books(user)
                        while True:
                            return_book_index = get_user_booklist(books_of_user)
                            if return_book_index == 'b':
                                break
                            
                            try:
                                x = input("[y] Confirm  [n] Modify\n")
                            
                                if x.lower() != 'y':
                                    continue
                                else:
                                    return_books(books_of_user,return_book_index,user)
                                    clear()
                                    break
                            except:
                                print("Invalid Selection. Please try again.")
                                continue
                    except:
                        print("\nNo Books Issued to you!\n")
                        continue
                if y == '3': #See books Issued to me
                    try:
                        books_of_user = get_issued_books(user)
                        print("\n")
                        for (i,book) in enumerate(books_of_user): 
                            print(i,book)
                        print("\n------------------------- End of List ------------------------------\n")
                        continue
                    except:
                        print("\nNo Books Issued to you!\n")
                        continue
                
                if y == '4':
                    change_password(user)
                continue
        else:
            while True:
                
                z = input("What would you like to do today?\n [1] Issue a Book    [2] See books Issued to user      [3] Return a book   \n [4] Block a user    [5] Unblock user                  [6] Change Password \n [7] See Available Book Stock                          [8] Delete a User\n")
                if z == 'b':
                    break
                if quit_app(z):
                    quit()
                    
                if z == '1': #Issue a Book
                    books_in_stock = data.loc[data['stock'] > 0,'name'].values.tolist()
                    while True:
                        user_to_issue = input("Please enter username for which to issue books:")
                        if user_to_issue == 'b':
                            break
                        if users.loc[users.role=='admin',].email.eq(user_to_issue).any():
                            print("This is an Admin user. Cannot proceed further!")
                            continue
                        elif not users.loc[users.role=='user',].email.eq(user_to_issue).any():
                            print("User does not exist! Try Again.")
                            continue
                        while True:
                            
                            to_issue = get_user_booklist(books_in_stock)
                            if to_issue == 'b':
                                break
                            
                            x = input("[y] Confirm  [n] Modify\n")
                            
                            if x.lower() != 'y':
                                continue
                            else:
                                # write function to add books to user
                                issue_books(books_in_stock,to_issue,user_to_issue)
                                break
                        break
                    continue
                    
                if z == '2': # See books Issued to user
                    try:
                        while True:
                            username_for_books = input("Please enter username for which to show issued list:")
                            if username_for_books == 'b':
                                break
                            
                            if users.loc[users.role=='admin',].email.eq(username_for_books).any():
                                print("This is an Admin user. Cannot proceed further!")
                                continue
                            elif users.loc[users.role=='user',].email.eq(username_for_books).any():
                                books_of_user = get_issued_books(username_for_books)
                                print("\n")
                                for (i,book) in enumerate(books_of_user): 
                                    print(i,book)
                                print("\n------------------------- End of List ------------------------------\n")
                                break
                            else:
                                print("Email Address does not exist! Try Again.")
                    except:
                        print("\nNo Books Issued to User!\n")
                        continue
                    continue
                
                if z == '3': # Return a book
                    try:
                        while True:
                            username_for_return = input("Please enter username for which to process a return:")
                            if username_for_return == 'b':
                                break
                            if users.loc[users.role=='admin',].email.eq(username_for_return).any():
                                print("This is an Admin user. Cannot proceed further!")
                                continue
                            elif users.loc[users.role=='user',].email.eq(username_for_return).any():
                                if len(list(filter(None,users.loc[users.email==username_for_return,'books_borrowed']))) == 0:
                                    raise ValueError('A very specific bad thing happened.')
                                break
                            else:
                                print("Email Address does not exist! Try Again.")
                        err = 0
                        
                        while True:
                            if err == 0:
                                books_of_user = get_issued_books(username_for_return)
                                #print(books_of_user)
                                #print(len(books_of_user))
                            return_book_index = get_user_booklist(books_of_user)
                                #print(return_book_index)
                                #print(username_for_return)
                            if return_book_index == 'b':
                                break
                            
                            try:
                                x = input("[y] Confirm  [n] Modify\n")
                            
                                if x.lower() != 'y':
                                    continue
                                else:
                                    return_books(books_of_user,return_book_index,username_for_return)
                                    err = 0
                                    clear()
                                    break
                            except:
                                print("Invalid Selection. Please try again.")
                                err = 1
                                
                                
                    except:
                        print("\nNo Books Issued to User!\n")
                        continue
                    
                    continue
                    
                if z == '4': # Block a user
                    while True:
                        if not users.loc[(users["role"]=='user'),'blocked'].eq(0).any():
                            print('No users available to be blocked!')
                            break
                        print(users.loc[(users["role"]=='user') & (users["blocked"]==0),].reset_index().email.to_string(),"\n")
                        user_index_to_block = input("Enter the number of the user to block:\n")
                        if user_index_to_block == 'b':
                            break
                        try:
                            
                            user_index_to_block = int(user_index_to_block)
                            username_to_block = list(users.loc[(users["role"]=='user') & (users["blocked"]==0),].reset_index().email)[user_index_to_block]
                            users.loc[users.email == username_to_block,'blocked'] = 1
                            users.to_csv('C:/Python/LMS/users.txt', sep=",", header=True,index=None)
                            print("User:",username_to_block, "has been Blocked from the system\n")
                            
                            break
                        except:
                            print("Invalid Input\n")
                    
                    continue
                    
                if z == '5':
                    if users.loc[(users["role"]=='user') & (users["blocked"]==1),].empty: # Unblock User
                        print("No user is blocked currently.\n")
                        continue
                    else:
                        while True:
                            print(users.loc[(users["role"]=='user') & (users["blocked"]==1),].reset_index().email.to_string(),"\n")
                            user_index_to_unblock = input("Enter the number of the user to unblock:\n")
                            if user_index_to_unblock == 'b':
                                break
                            try:
                                user_index_to_unblock = int(user_index_to_unblock)
                                #print(list(users.loc[(users["role"]=='user') & (users["blocked"]==1),].reset_index().email))
                                username_to_unblock = list(users.loc[(users["role"]=='user') & (users["blocked"]==1),].reset_index().email)[user_index_to_unblock]
                                #print(username_to_unblock)
                                users.loc[users.email == username_to_unblock,'blocked'] = 0
                                users.to_csv('users.txt', sep=",", header=True,index=None)
                                print("User:",username_to_unblock, "has been unblocked!\n")
                                break
                            except:
                                print("Invalid Input\n")
                    continue       
                
                if z == '6':
                    print(user)
                    change_password(user)
                    continue
                
                if z == '7':
                    show_booklist('instock',user)
                    continue
                    
                if z == '8':
                    print(users.loc[(users["role"]=='user'),].reset_index().email.to_string(),"\n")
                    while True:
                        user_to_delete = input("Please enter username that you want to delete:")
                        if user_to_delete == 'b':
                            break
                        if users.loc[users.role=='admin',].email.eq(user_to_delete).any():
                            print("This is an Admin user. Cannot proceed further! \n")
                            continue
                        elif not users.loc[users.role=='user',].email.eq(user_to_delete).any():
                            print("User does not exist! Try Again. \n")
                            continue
                        elif len(list(filter(None,users.loc[users.email==user_to_delete,'books_borrowed']))) > 0:
                            print("\nThis user has issued books. Please return those before deleting! \n")
                            break
                        
                        drop_index = users[(users.email==user_to_delete)].index
                        users = users.drop(drop_index)
                        break
                    continue
                    
                print("\nInvalid Input\n")
            
    if x == '2': # Create new User
        clear()
        new_user = None
        pwd = None
        while True:
            if new_user is None:
                new_user = input("\nPlease enter your new usename:")
                
                if new_user == 'b': 
                    break
                if users.email.eq(new_user).any():
                    print("Username already exists! Try Again.")
                    continue
            if pwd is None:    
                pwd = getpass.getpass("\nPlease enter your new password:")
                pwd1 = getpass.getpass("\nPlease confirm your new password:")
                if pwd != pwd1:
                    print("Passwords do not match! Try Again.")
                    pwd = None
                    continue
        
            new_role = input("\nPlease select a role\n[u] User    [a] admin\n")

            if new_role not in ['u','a']:
                print("Invalid Selection! Try Again.")
                continue
            elif new_role == 'u':
                new_role = 'user'
                break
            else:
                new_role = 'admin'
                break
        
            users = users.append({'email':new_user, 'password':pwd, 'role':new_role, 'blocked':0, 'books_borrowed':''}, ignore_index=True)
            users.to_csv('users.txt', sep=",", header=True,index=None)
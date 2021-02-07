# -*- coding: utf-8 -*-
from jose import jwt
# from settings import SECRET_KEY
import secrets
SECRET_KEY=secrets.token_hex(256)

def token_gen(user_data:dict):
    
    
    token=jwt.encode(user_data, SECRET_KEY, algorithm='HS256')
    return token

def token_decode(token:str):
    values = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return values



if __name__=="__main__":
    user_data={'user_name':'bob',"admin":True,"favorite_color":"blue"}
    token = token_gen(user_data=user_data)
    print(token)
    values=token_decode(token=token)
    print(values)
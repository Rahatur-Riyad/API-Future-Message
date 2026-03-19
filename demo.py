import bcrypt

x = input("Enter")
print(bcrypt.checkpw(x,"$2b$12$gpAmgdMu73Ndj5ZPzJpzsuj2.DuBET.Z4oLlRDrvq8HHE3VFbe3rK"))

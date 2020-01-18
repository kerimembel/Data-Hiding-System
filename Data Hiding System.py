from tkinter import Button, Entry, Frame, Label, Tk, filedialog, messagebox
import os
from tkinter.ttk import Combobox, Notebook
import cripto_module
import stego_module

class Application(Frame):

        def __init__(self, master):
                Frame.__init__(self, master)
                self.create_widgets()
                self.text_filename = ""
                self.image_filename = ""
                self.currdir = os.getcwd()
                self.IsEncrypted = False

        def create_widgets(self):
                #Creating Encrypt Tab
                TAB_CONTROL = Notebook(master)
                encrypt_tab = Frame(TAB_CONTROL)
                TAB_CONTROL.add(encrypt_tab, text='Encrypt')

                #Creating Decrypt Tab
                decrypt_tab = Frame(TAB_CONTROL)
                TAB_CONTROL.add(decrypt_tab, text='Decrypt')

                TAB_CONTROL.pack(expand=1, fill="both")

                Label(encrypt_tab,
                        text="Text File").grid(row=0,column=0,padx=10, pady=20)
                Label(encrypt_tab,
                        text="Cover Image").grid(row=6,column=0,padx=10, pady=20)
                Label(decrypt_tab,
                        text="Cipher File").grid(row=4,column=0,padx=10, pady=20)
                Label(decrypt_tab,
                        text="Stego Image").grid(row=0,column=0,padx=10, pady=20)
                Label(encrypt_tab,
                        text = "Encryption Algorithm").grid(row=2,column=0,padx=10,pady=20)
                Label(decrypt_tab,
                        text = "Decryption Algorithm").grid(row=6,column=0,padx=10,pady=20)

                self.enc_key_label = Label(encrypt_tab, text = "Key").grid(row=4,column = 0)
                self.dec_key_label = Label(decrypt_tab, text = "Key").grid(row=8,column = 0)
                self.textfile_entry = Entry(encrypt_tab,width="40",state='disabled')
                self.ciphertext_entry = Entry(decrypt_tab,width="40",state='disabled')
                self.coverimage_entry = Entry(encrypt_tab,width="40",state='disabled')
                self.encryptkey_entry = Entry(encrypt_tab,width="40",show="*")
                self.stegoimage_entry = Entry(decrypt_tab,width="40",state='disabled')
                self.decryptkey_entry = Entry(decrypt_tab,width="40",show="*")


                self.textfile_entry.grid(row = 0,column = 2,padx=10,pady=10,ipady=3)
                self.coverimage_entry.grid(row = 6,column = 2,padx=10,pady=10,ipady=3)
                self.encryptkey_entry.grid(row = 4,column = 2,padx=10)
                self.stegoimage_entry.grid(row = 0,column = 2,padx=10,pady=10,ipady=3)
                self.decryptkey_entry.grid(row = 8,column = 2,padx=10)
                self.ciphertext_entry.grid(row = 4 ,column = 2,padx =10)

                algorithms=("AES", "DES","Triple DES")
                self.enc_algorithm_list=Combobox(encrypt_tab, values=algorithms)
                self.enc_algorithm_list.grid(row = 2, column = 2)
                self.dec_algorithm_list=Combobox(decrypt_tab, values=algorithms)
                self.dec_algorithm_list.grid(row = 6, column = 2)

                self.browse_text_button = Button(encrypt_tab,text='Choose Text File',
                        command=self.search_for_text, width='20').grid(row=0, column=3)

                self.browse_image_button = Button(encrypt_tab,text='Choose Cover Image',
                        command=self.search_for_image, width='20').grid(row=6, column=3,padx=20,pady=30)

                self.encrypt_button = Button(encrypt_tab,text='Encrpyt File',
                        command = self.encrypt,width='20').grid(row =4 ,column = 3)

                self.hide_button = Button(encrypt_tab,text='Hide File',
                        command = self.hide_data,width='20').grid(row =8 ,column = 3)

                self.browse_cipher_button = Button(decrypt_tab,text='Choose Cipher File',
                        command=self.search_for_cipher, width='20').grid(row=4, column=3)

                self.browse_stego_button = Button(decrypt_tab,text='Choose Stego Image',
                        command=self.search_for_stego, width='20').grid(row=0, column=3)

                self.decrypt_button = Button(decrypt_tab,text='Decrypt File',
                        command = self.decrypt,width='20').grid(row = 8 ,column = 3)

                self.extract_button = Button(decrypt_tab,text='Extract File',
                        command = self.extract_data,width='20').grid(row = 2 ,column = 3,padx=20,pady=20)


        def encrypt(self):

                if((self.textfile_entry.get() != '') &  (self.enc_algorithm_list.get()!= '') & (self.encryptkey_entry.get() != '')):
                        cripto_module.encrypt_file(self.text_filename,self.enc_algorithm_list.get(),self.encryptkey_entry.get())
                        self.IsEncrypted = True
                        messagebox.showinfo("Success", "Encryption succesfull!")
                else:
                        messagebox.showerror("Error", "Please fill necessary areas!")

        def extract_data(self):
                if(self.stegoimage_entry.get() != ''):
                        stego_module.decode(self.stegoimage_entry.get())
                        messagebox.showinfo("Success", "Extraction succesfull!")

                else:
                        messagebox.showerror("Error", "Please fill necessary areas!")


        def hide_data(self):
                if((self.coverimage_entry.get() != '') & (self.textfile_entry.get() != '')):
                        if(self.IsEncrypted):
                                try:           
                                                      
                                        stego_module.encode(self.image_filename,self.text_filename)                       
                                except ValueError as v:
                                        messagebox.showerror("Error", "Data is too large for this image!")
                                        return

                        else:
                                messagebox.showwarning("Warning!","You did not encrypt the message.\nWe suggest the encrypt message before hiding.")
                                return

                        messagebox.showinfo("Success", "Hiding into image is succesfull!")
                else:
                        messagebox.showerror("Error", "Please fill necessary areas!")



        def decrypt(self):

                if((self.ciphertext_entry.get() != '') & (self.dec_algorithm_list.get()!= '') & (self.decryptkey_entry.get() != '')):
                        try:
                                cripto_module.decrypt_file(self.text_filename,self.dec_algorithm_list.get(),self.decryptkey_entry.get())
                        except UnboundLocalError as u :
                                messagebox.showerror("Error", "Did you choose correct Algorithm?")
                                raise UserWarning("Type Error\n",u.__traceback__)

                        except TypeError as t:
                                messagebox.showerror("Error", "Did you choose correct Algorithm?")
                                raise UserWarning("Type Error\n",t.__traceback__)

                        except UserWarning as u:
                                messagebox.showerror("Error","Might be wrong key!!")
                        
                        messagebox.showinfo("Success", "Decryption succesfull!")

                else:
                        messagebox.showerror("Error", "Please fill all areas!.")


        def search_for_text(self):
                filename = filedialog.askopenfilename(initialdir = self.currdir,
                                title = "Select A Text File",
                                filetype = (("text files","*.txt"),("all files","*.*")))
                self.text_filename = filename
                self.textfile_entry.config(state='normal')
                self.textfile_entry.delete(0,'end')
                self.textfile_entry.insert(0,os.path.basename(self.text_filename))
                self.textfile_entry.config(state='disabled')
                self.IsEncrypted = False


        def search_for_image(self):
                filename = filedialog.askopenfilename(initialdir = self.currdir,
                                title = "Select A Cover Image",
                                filetype = (("PNG files","*.png"),("all files","*.*")))
                self.image_filename = filename
                self.coverimage_entry.config(state='normal')
                self.coverimage_entry.delete(0,'end')
                self.coverimage_entry.insert(0,os.path.basename(self.image_filename))
                self.coverimage_entry.config(state='disabled')

        def search_for_cipher(self):
                filename = filedialog.askopenfilename(initialdir = self.currdir,
                                title = "Select A Text File",
                                filetype = (("text files","*.enc"),("all files","*.*")))
                self.text_filename = filename
                self.ciphertext_entry.config(state='normal')
                self.ciphertext_entry.delete(0,'end')
                self.ciphertext_entry.insert(0,os.path.basename(self.text_filename))
                self.ciphertext_entry.config(state='disabled')


        def search_for_stego(self):
                filename = filedialog.askopenfilename(initialdir = self.currdir,
                                title = "Select A Stego Image",
                                filetype = (("PNG files","*.png"),("all files","*.*")))
                self.image_filename = filename
                self.stegoimage_entry.config(state='normal')
                self.stegoimage_entry.delete(0,'end')
                self.stegoimage_entry.insert(0,os.path.basename(self.image_filename))
                self.stegoimage_entry.config(state='disabled')


if(__name__=="__main__"):
        master = Tk()
        master.title("Data Hiding System")
        master.geometry("700x500+10+20")

        app = Application(master)
        master.mainloop()



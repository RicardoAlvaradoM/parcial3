# -*- coding: utf-8 -*-
import web
import json
from data import data
from web import form

db = web.database(dbn='mysql', db='mydb', user='root', pw='root')
render = web.template.render('views/', base = 'base')

urls=(
    '/','index',
    '/leer(.*)','datos',
    '/buscar(.*)','buscar',
    '/mapa(.*)','mapa',
    '/login','login',
    '/acceso','acceso',
    '/nuevo','nuevo',
    '/editar/(.+)','editar',
    '/ver/(.+)','ver',
    '/eliminar/(.+)','eliminar'
)
data = data()
data.read()
myformBusqueda = form.Form(
    form.Dropdown('Descripcion',data.getDescripcion()),
    form.Dropdown('Unico', data.getUnitId())
)
myformLogin = form.Form(
    form.Textbox("Usuario"),
    form.Password("Clave")
)
myformComunidad = form.Form(
    form.Textbox("Nombre"),
    form.Textbox("No"),
    form.Textbox("Longitud"),
    form.Textbox("Latitud")
)
class login:
    def GET(self):
        form = myformLogin()
        return render.login(form)
    def POST(self):
        form = myformLogin()
        if not form.validates():
            return render.Login(form)
        else:
            result = db.select('usuarios')
            dbUser=""
            dbPassw=""
            for row in result:
                dbUser=row.user
                dbPassw=row.passw
            if dbUser==form.d.Usuario and dbPassw==form.d.Clave:
                raise web.seeother("/acceso")
            else:
                return "Usuario y/o contraseña incorrecta"

class acceso:
    def GET(self):
        result=db.select('comunidad')
        return render.acceso(result)
    def POST(self):
        raise web.seeother("/nuevo")
class nuevo:
    def GET(self):
        formNew = myformComunidad()
        return render.nuevo(formNew)
    def POST(self):
        formNew = myformComunidad()
        if not formNew.validates():
            return render.nuevo(formNew)
        else:
            db.insert('comunidad',
            Nombre=formNew.d.Nombre, 
            No_Hab=formNew.d.No,
            Longitud=formNew.d.Longitud,
            Latitud=formNew.d.Latitud)
            raise web.seeother("/acceso")
class editar:
    def GET(self,id):
        formEdit=myformComunidad()
        result=db.select('comunidad', where= "id=%s"%(id))

        for row in result:
            formEdit['Nombre'].value=row.Nombre
            formEdit['No'].value=row.No_Hab
            formEdit['Longitud'].value=row.Longitud
            formEdit['Latitud'].value=row.Latitud
        return render.editar(formEdit)

    def POST(self,id):
        formEdit=myformComunidad()
        if not  formEdit.validates():
            return render.editar(formEdit)
        else:
            db.update('comunidad',where="id=%s"%(id),
            Nombre=formEdit.d.Nombre,
            No_Hab=formEdit.d.No,
            Longitud = formEdit.d.Longitud,
            Latitud = formEdit.d.Latitud
             )
            raise web.seeother("/acceso")
class eliminar:
    def GET(self,id):
        formEdit=myformComunidad()
        result=db.select('comunidad', where= "id=%s"%(id))

        for row in result:
            formEdit['Nombre'].value=row.Nombre
            formEdit['No'].value=row.No_Hab
            formEdit['Longitud'].value=row.Longitud
            formEdit['Latitud'].value=row.Latitud
        return render.eliminar(formEdit)

    def POST(self,id):
        formEdit= myformComunidad()
        if not formEdit.validates():
            return render.eliminar(formEdit)
        else:
            db.delete('comunidad', where="id=%s"%(id))
            raise web.seeother("/acceso")
class ver:
    def GET(self,id):
        result=db.select('comunidad', where="id=%s"%(id))
        return render.ver(result)


class datos:
    def GET(self,data):
        data=[]
        with open('data/data.json','r')as file:
            data=json.load(file)
        return render.datos(data['Items'])
    


class mapa:
    def GET(self,data):
        data=[]
        with open('data/data.json','r')as file:
            data=json.load(file)
        return render.mapa(data['Items'])
class buscar:
    def GET(self,results):
        form = myformBusqueda
        return render.buscar(form, None)
    def POST(self, results):
        form = myformBusqueda
        if not form.validates():
             return render.buscar(form)
        else:
            user_data = web.input()
            descripcion = user_data.Descripcion
            unico = user_data.Unico
            results = data.getLocation(descripcion, unico)
            return render.buscar(form, results)
class index:
    def GET(self):
        return render.index()
if __name__ == "__main__":
    app = web.application(urls, globals())
    web.config.debug = True
    app.run()
    
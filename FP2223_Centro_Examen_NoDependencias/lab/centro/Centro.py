'''
Created on 22 nov 2022

@author: belen
'''
from __future__ import annotations
from lab.centro.Alumno import Alumno
from lab.centro.Profesor import Profesor
from lab.centro.Asignatura import Asignatura
from lab.centro.Matricula import Matricula
from lab.centro.Asignacion import Asignacion
from typing import Iterable, Optional
from tools.File import absolute_path, lineas_de_fichero
from tools.Iterable import strfiter

class Centro:
    
    centro = None

    def __init__(self, alumnos:list[Alumno], profesores:list[Profesor],asignaturas:list[Asignatura],\
            matriculas:set[Matricula], \
            asignacion_de_profesores:set[Asignacion])->None:
        self.alumnos = alumnos
        self.profesores = profesores
        self.asignaturas = asignaturas
        self.matriculas = matriculas
        self.asignacion_de_profesores = asignacion_de_profesores 
        
        self.alumnos_dni:dict[str,Alumno] = {a.dni : a for a in self.alumnos}
        self.profesores_dni:dict[str,Profesor] = {p.dni : p for p in self.profesores}
        

    @staticmethod
    def of()->Centro:
        if Centro.centro is None:
            Centro.centro = Centro.of_files()
        return Centro.centro

        
    @staticmethod
    def of_files(fichero_alumnos:str=absolute_path('/ficheros/alumnos.txt'),
           fichero_profesores:str=absolute_path('/ficheros/profesores.txt'),
           fichero_asignaturas:str=absolute_path('/ficheros/asignaturas.txt'))->Centro:
        alumnos:list[Alumno] = [Alumno.parse_alumno(ln) for ln in 
                                lineas_de_fichero(fichero_alumnos,encoding='utf-8')]
        profesores:list[Profesor] = [Profesor.parse_profesor(ln) for ln in lineas_de_fichero(fichero_profesores,encoding='utf-8')]
        asignaturas:list[Asignatura] = [Asignatura.parse(ln) for ln in lineas_de_fichero(fichero_asignaturas,encoding='utf-8')]
        Centro.centro = Centro(alumnos,profesores,asignaturas,set(),set())
        return Centro.centro
    
    def add_asignaciones(self,fichero:str=absolute_path('/ficheros/asignaciones.txt'))->None:
        r:Iterable[Asignacion] = (Asignacion.parse(ln)  
                                  for ln in lineas_de_fichero(fichero))       
        for a in r:
            self.asignacion_de_profesores.add(a)
               
    def add_asignacion(self,profesor:Profesor,asignatura:Asignatura,grupo:int)->None:
        self.asignacion_de_profesores.add(Asignacion.of(profesor.dni,asignatura.id,grupo))      
    
    def add_matriculas(self,fichero:str=absolute_path('/ficheros/matriculas.txt'))->None:
        r:Iterable[Matricula] = (Matricula.parse(ln)  for ln in lineas_de_fichero(fichero))       
        for a in r:
            self.matriculas.add(a)
            
    def add_matricula(self,alumno:Alumno,asignatura:Asignatura,grupo:int)->None:
        self.matriculas.add(Matricula.of(alumno.dni,asignatura.id,grupo))
    
    @property
    def numero_profesores(self)->int: 
        return len(self.profesores)
    
    @property
    def numero_alumnos(self)->int: 
        return len(self.alumnos)
    
    @property
    def numero_asignaturas(self)->int: 
        return len(self.asignaturas)
    
    @property
    def numero_grupos(self)->int: 
        return sum(a.num_grupos for a in self.asignaturas)
    
    def profesor(self,i:int)->Profesor: 
        return self.profesores[i]
    
    def profesor_de_dni(self,dni:str)->Profesor: 
        return self.profesores_dni[dni]
    
    def alumno_de_dni(self,dni:str)->Alumno: 
        return self.alumnos_dni[dni]
    
    def asignatura(self,i:int)->Asignatura: 
        return self.asignaturas[i]
    
    def alumno(self,i:int)->Alumno: 
        return self.alumnos[i]
    
    def asignaturas_impartidas(self,profesor:Profesor)->set[Asignatura]: 
        return {self.asignatura(asg.ida) 
                for asg in Centro.of().asignacion_de_profesores if asg.dni == profesor.dni}
    
    def asignaturas_cursadas(self,alumno:Alumno)->set[Asignatura]: 
        return {self.asignatura(m.ida) for m in Centro.of().matriculas if m.dni == alumno.dni}
    
    #===========================================================================
    # DEFENSA
    #===========================================================================
    def alumnos_con_letra_dni(self, lt:str)->list[Alumno]:
        return [a for a in self.alumnos if lt in a.dni]
    
    
    def asignaturas_no_impartidas(self, pr:Profesor)->set[Asignatura]:
        return set(a for a in self.asignaturas if a not in self.asignaturas_impartidas(pr))
    
    def numero_asignaturas_alumno(self, al:Alumno)->int:
        return len(self.asignaturas_cursadas(al))
    
    @property
    def edad_media_alumnos(self)->Optional[int]:
        if self.numero_alumnos>0:
            al_mayores:list[int] = [a.edad for a in self.alumnos if a.edad >=18]
            return int(sum(al_mayores)/len(al_mayores))
        else:
            return None
        

        
        
        

if __name__ == '__main__':
    Centro.of()
    print(f'- Hay {Centro.of().numero_alumnos} alumnos en el centro')
    print(f'- Hay {Centro.of().numero_profesores} profesores en el centro')
    print(f'- Hay {Centro.of().numero_asignaturas} asignaturas en el centro')
    print(f'- Hay {Centro.of().numero_grupos} grupos en el centro')

    
    print('___________')
    print(">> Añadiendo asignaciones")
    Centro.of().add_asignaciones()
    print('- El número de asignaciones es:')    
    print(len(Centro.of().asignacion_de_profesores))
    
    print('___________')
    print(">> Añadiendo matrículas")
    Centro.of().add_matriculas()
    print('- El número de matrículas es:')
    print(len(Centro.of().matriculas))
    print('___________')
    
    
    p = Centro.of().profesor_de_dni('53045701L')
    print(f'- El profesor con dni 53045701L es {p}')
    print('___________')
    
    
    print(f'- Las asignaturas impartidas por {p.nombre} son:')
    print(strfiter((a.nombre for a in Centro.of().asignaturas_impartidas(p)),sep='\n',prefix='',suffix=''))
    print('___________')
    
    al = Centro.of().alumno(200)
    print(f'- El alumno que se encuentra en la posición 200 es {al}')
    print('___________')

    print(f'- Las asignaturas cursadas por {al.nombre} son:')
    print(strfiter((a.nombre for a in Centro.of().asignaturas_cursadas(al)),sep='\n',prefix='',suffix=''))
    print('___________')   
    
    print(f'- Hay un total de {Centro.of().numero_grupos} grupos.')
    print('___________') 
    

    
    
    

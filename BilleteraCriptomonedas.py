import requests
from datetime import date

#Testing if menu actio is correct
def esopcion (menu):
  return esnumeroentero(menu) and 7>int(menu)>0
      
def esmoneda(cripto):
    return cripto in monedas

def esnumero(numero): 
    return numero.replace('.','',1).isdigit()
  
def esnumeroentero(numero): 
    return numero.isdigit()

def escodigo(numero): 
    return esnumeroentero(numero) and int(numero)!=codigo_propio

def monedaEnBalance(moneda):
  return moneda in monedas_balance

def PreguntarMoneda(tipoTransaccion):
  moneda=input('Indique el nombre de la moneda a '+ tipoTransaccion+':' )
  while not esmoneda(moneda):
      print('')
      print('Moneda Invalida.')
      print('')
      moneda=input('Indique el nombre de la moneda a '+ tipoTransaccion+':' )
  return moneda

def PreguntarCantidad(moneda):
  cantidad = input('Indique la cantidad de '+moneda+':')
  while not esnumero(cantidad):
    print('')
    print('Cantidad Invalida.')
    print('')
    cantidad = input("Indique la cantidad de "+moneda+":")
  return cantidad

def PedirCodigo(tipo_receptor):
  codigo = input('Indique código del '+ tipo_receptor+ ' (Este es un valor numérico entero):')
  while not escodigo(codigo):
    print('')
    print('Código Invalido.')
    print('')
    codigo = input('Indique código del '+ tipo_receptor+ ' valido:')
  return codigo
    
def RegistrarTransaccion(moneda,tipo,codigo,cantidad,monto):
    today=date.today()
    transaccion=[]
    transaccion.append(str(today))
    transaccion.append(moneda)
    transaccion.append(tipo)
    transaccion.append(codigo)
    transaccion.append(cantidad)
    transaccion.append(monto)
    transacciones.append(transaccion)
    
def RecibirTransaccion():
  print('')
  moneda=PreguntarMoneda('recibir')  
  cantidad = PreguntarCantidad(moneda)
  codigo = PedirCodigo('remitente')
  
  if monedaEnBalance(moneda):
    monedas_balance_dic[moneda]=monedas_balance_dic[moneda]+ float(cantidad)
    RegistrarTransaccion(moneda,'Recepción',codigo,cantidad,monedas_dic[moneda])
    print('')
    print('Se agregaron a la cuenta ',cantidad,'', moneda)
    print('')
   
  else:
    monedas_balance_dic[moneda]=float(cantidad)
    RegistrarTransaccion(moneda,'Recepción',codigo,cantidad,monedas_dic[moneda])
    print('')
    print('Se agregaron a la cuenta ',cantidad,'', moneda)
    print('')

def TransferirMonto():
  print('')
  moneda=PreguntarMoneda('transferir')
  if not monedaEnBalance(moneda):
    print('')
    print('No tiene saldo de', moneda)
    print('')
  else:
    cantidad= PreguntarCantidad(moneda)
    if float(cantidad)>monedas_balance_dic[moneda]:
      print('')
      print('No tiene el saldo suficiente para hacer esta transacción!')
      print('')

    else:
      codigo = PedirCodigo('destinatario')
      print('')
      print('Se debitaron de la cuenta ',cantidad,'', moneda)
      print('')
      monedas_balance_dic[moneda]=monedas_balance_dic[moneda]-float(cantidad)
      if monedas_balance_dic[moneda]==0:
        del monedas_balance_dic[moneda]
        
      RegistrarTransaccion(moneda,'Envío    ',codigo,cantidad,monedas_dic[moneda])
  
def MostrarBalanceMoneda():
  print('')
  moneda = moneda=PreguntarMoneda('consultar')
  print('')
  print('Balance de ',moneda )
  print('')
  
  if monedaEnBalance(moneda):
    equivalencia=monedas_dic[moneda]*monedas_balance_dic[moneda]
    print('Tiene ',monedas_balance_dic[moneda],'' , moneda, ' que equivalen a %6.3f'%equivalencia+' USD')
    print('')
  else:
    print('No posee esta moneda en su portafolio!')
    print('')

def MostrarBalanceGeneral():
  print('')
  print('Balance general')
  print('')
  print('Nombre   Cantidad   Valor en USD     Total Moneda en USD')
  total_USD=0
  for moneda in monedas_balance_dic:
    USDequivalente=monedas_dic[moneda] * monedas_balance_dic[moneda]
    print (moneda, '       ',monedas_balance_dic[moneda], '       %10.3f'%monedas_dic[moneda]+ '     %15.3f'%USDequivalente   )
    total_USD+=USDequivalente
  print('')
  print('USD Totales: $%15.3f'%total_USD+' USD')
  print('')
    

def MostrarTransacciones():
  print('')
  print('Historial de Transacciones')
  print('')
  print('Fecha        Moneda   Tipo de Operación  Código de usuario   Cantidad    USD al momento')
  for registro in transacciones:
    print (registro[0], '   ',registro[1], '       ',registro[2], '        ',registro[3] , '               ',registro[4], '   %15.3F '%registro[5]  )

  print('')
  
#Asignación del codigo del usuario
codigo_propio=132

monedas=()
monedas_dic={}
monedas_balance=()
monedas_balance_dic={}
transacciones=[]


#Query of criptos to coinmarketcap.com

def TraerDatos():
  
    COINMARKET_API_KEY = "2448e9c9-b938-4f0e-85f1-9878a7b41c87"
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': COINMARKET_API_KEY
    }
    data=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",headers=headers).json()
    for id in data["data"]:
        monedas_dic[id["symbol"]]=id["quote"]["USD"]["price"]
    
  

while 1:
  
  TraerDatos()
  monedas=monedas_dic.keys()
  print("Menú de Billetera digital: ");
  print("   1. Recibir cantidad");
  print("   2. Transferir monto");
  print("   3. Mostrar balance una moneda");
  print("   4. Mostrar balance general");
  print("   5. Mostrar histórico de transacciones");
  print("   6. Salir del programa");
  monedas_balance=monedas_balance_dic.keys()
  
  menu=input("Ingrese el número de la acción que desea realizar:");
  while not esopcion(menu):
    menu=input("Acción NO VALIDA!. Ingrese el número de la acción que desea realizar:");

  if menu=="1":
    RecibirTransaccion() 

  if menu=="2":
    TransferirMonto()

  if menu=="3":
    MostrarBalanceMoneda()

  if menu=="4":
    MostrarBalanceGeneral()

  if menu=="5":
    MostrarTransacciones()

  if menu=="6":
    print('')
    print('Se cerró la apricación, ¡Hasta Pronto!')
    break




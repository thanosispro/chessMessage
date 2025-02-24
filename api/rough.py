
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.renderers import JSONRenderer
import os
from .stockfish import opponent
from asgiref.sync import sync_to_async
from adrf.decorators import api_view
import asyncio
from stockfish import Stockfish
from django.contrib.staticfiles.storage import staticfiles_storage

stockfish_path = 'C:/Users/user/Downloads/stockfish/stockfish-windows-x86-64-avx2.exe'

print(os.curdir)



engine =Stockfish(stockfish_path)

engine.set_depth(15)

# some asynnc function
@sync_to_async
def get_async_evaluation():
    return  engine.get_evaluation()

@sync_to_async
def get_async_best_move():
    return  engine.get_best_move()
# Create your views here.

@api_view(['GET'])
@parser_classes([JSONRenderer])
async def enginePost(request):


    fen = request.GET.get('fen')
    depth = request.GET.get('depth')    
    engine.set_fen_position(fen)
    
    best_move =  await asyncio.gather(get_async_best_move())
    print(best_move[0])
    return Response({'value':str(best_move)})


@api_view(['GET'])
@parser_classes([JSONRenderer])
async def getCp(request):
    global engine
    print('hello world')
    
    best_cp=0

    fen = request.GET.get('fen')
    turn = int(request.GET.get('turn'))
    
    previous_best_cp = request.GET.get('best_cp')
    best_move = await asyncio.gather(get_async_best_move())
    best_move = best_move[0]
    engine.make_moves_from_current_position([])
    
    
    
    info =  await asyncio.gather(get_async_evaluation())
    info = info[0]
    if info['type'] == "mate":
        return Response({'best_cp':previous_best_cp})
    if turn==1:
        best_cp = info['value']*1
    elif turn==2:
        best_cp = info['value']*-1
    
    return Response({'best_cp':best_cp})


@api_view(['GET'])
@parser_classes([JSONRenderer])
async def engineGet(request):
    global engine
    
    cp=0
    data= request.data
    fen = request.GET.get('fen')
    
    
    
    turn = int(request.GET.get('turn'))
    previous_best_cp = int(request.GET.get('best_cp'))
    previous_cp = int(request.GET.get('cp'))
    
    engine.set_fen_position(fen)
    winning=''
    
    
    info =  await asyncio.gather(get_async_evaluation())
    info = info[0]
    if info['type'] == "mate":
        mate_move = info.get('score').relative.score(mate_score=True)
        total_move = f"Mate in {mate_move}"
        return Response({'value':total_move,'cp':previous_cp,'best_cp':previous_best_cp})
    if turn == 1:

        cp = info['value']*1
    elif turn == 2:

        cp = info['value']*-1

    if info["value"] > 0:
        winning='You are winning'
    elif info["value"] < 0:
        winning='You are losing'
    else:
        winning='Balanced position'






    
    value = opponent(cp,previous_cp,previous_best_cp)




    return Response({'value':value,'cp':cp,'winning':winning})


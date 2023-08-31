# from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
import json
from itertools import product

x_axis = ["A","B","C","D","E","F","G","H"]

class Pieces(APIView):
    def post(self, request, slug):
        params = json.loads(request.body)
        positions = params.get("postions")
        response = Moves(slug).checking_valid_moves(positions)
        return JsonResponse({"valid_moves" : response}, status=200)


class Moves():
    def __init__(self, slug):
        self.slug = slug

    def checking_valid_moves(self, positions): 
        queen_pos = positions.get("Queen")
        bishop_pos = positions.get("Bishop")
        rook_pos = positions.get("Rook")
        knight_pos = positions.get("Knight")
        queen = list(self.queen_moves(queen_pos, bishop_pos, rook_pos, knight_pos))
        bishop = list(self.bishop_moves(queen_pos, bishop_pos, rook_pos, knight_pos))
        rook = list(self.rook_moves(queen_pos, bishop_pos, rook_pos, knight_pos))
        knight = list(self.knight_moves(queen_pos, bishop_pos, rook_pos, knight_pos))

        if self.slug == "queen":
            queen = [x for x in queen if x not in bishop if x not in rook if x not in knight]
            return queen

        if self.slug == "bishop":
            bishop = [x for x in bishop if x not in queen if x not in rook if x not in knight]
            return bishop
        
        if self.slug == "rook":
            rook = [x for x in rook if x not in queen if x not in bishop if x not in knight]
            return rook
        
        if self.slug == "knight":
            knight = [x for x in knight if x not in queen if x not in bishop if x not in rook]
            return knight

    def queen_moves(self, queen_pos, bishop_pos, rook_pos, knight_pos):
        x_pos = queen_pos[0]
        y_pos = queen_pos[1]
        valid_spots = self.straight_moves(x_pos, y_pos, queen_pos, bishop_pos, rook_pos, knight_pos)
        cross_valid_path = self.cross_move(x_pos, y_pos, queen_pos, bishop_pos, rook_pos, knight_pos)
        valid_spots.extend(cross_valid_path)
        return valid_spots

    def bishop_moves(self, queen_pos, bishop_pos, rook_pos, knight_pos):
        x_pos = bishop_pos[0]
        y_pos = bishop_pos[1]
        valid_spots = self.cross_move(x_pos, y_pos, queen_pos, bishop_pos, rook_pos, knight_pos)
        return valid_spots

    def rook_moves(self, queen_pos, bishop_pos, rook_pos, knight_pos):
        x_pos = rook_pos[0]
        y_pos = rook_pos[1]
        valid_spots = self.straight_moves(x_pos, y_pos, queen_pos, bishop_pos, rook_pos, knight_pos)
        return valid_spots

    def knight_moves(self, queen_pos, bishop_pos, rook_pos, knight_pos):
        valid_spots = []
        x_pos = int(x_axis.index(knight_pos[0]))
        y_pos = int(knight_pos[1])
        valid_spots.extend(product([x_pos-1, x_pos+1],[y_pos-2, y_pos+2]))
        valid_spots.extend(product([x_pos-2, x_pos+2],[y_pos-1, y_pos+1]))
        valid_spots = [str(x_axis[x_pos]) + str(y_pos) for x_pos, y_pos in valid_spots if y_pos > 0 if x_pos < 8]
        return valid_spots

    def straight_moves(self, x_pos, y_pos, queen_pos, bishop_pos, rook_pos, knight_pos):
        valid_spots = []
        # upward movement
        for i in range(int(y_pos)+1,9):
            path = x_pos + str(i)
            valid_spots.append(path)
            if path == queen_pos or path == bishop_pos or path == rook_pos or path == knight_pos:
                break

        # downward movement
        for i in reversed(range(1, int(y_pos))):
            path = x_pos + str(i)
            valid_spots.append(path)
            if path == queen_pos or path == bishop_pos or path == rook_pos or path == knight_pos:
                break

        # left movement
        for i in reversed(range(0, x_axis.index(x_pos))):
            path = x_axis[i] + y_pos
            valid_spots.append(path)
            if path == queen_pos or path == bishop_pos or path == rook_pos or path == knight_pos:
                break

        # right movement
        for i in range(x_axis.index(x_pos)+1,len(x_axis)):
            path = x_axis[i] + y_pos
            valid_spots.append(path)
            if path == queen_pos or path == bishop_pos or path == rook_pos or path == knight_pos:
                break
                
        return valid_spots

    def cross_move(self, x_pos, y_pos, queen_pos, bishop_pos, rook_pos, knight_pos):
        valid_spots = []
        # x_pos index in x_axis list
        x_pos_index = x_axis.index(x_pos)
       
        # cross left upwards
        for i,j in zip(reversed(range(0, x_pos_index)), range(int(y_pos)+1, 9)):
            path = x_axis[i] + str(j)
            valid_spots.append(path)
            if path == queen_pos or path == bishop_pos or path == rook_pos or path == knight_pos:
                break

        # cross right downwards
        for i,j in zip(range(x_pos_index+1, len(x_axis)), reversed(range(1, int(y_pos)))):
            path = x_axis[i] + str(j)
            valid_spots.append(path)
            if path == queen_pos or path == bishop_pos or path == rook_pos or path == knight_pos:
                break
        
        # cross right upwards
        for i,j in zip(range(x_pos_index+1, len(x_axis)), range(int(y_pos)+1, 9)):
            path = x_axis[i] + str(j)
            valid_spots.append(path)
            if path == queen_pos or path == bishop_pos or path == rook_pos or path == knight_pos:
                break
        
        # cross left downwards
        for i,j in zip(reversed(range(0, x_pos_index)), reversed(range(1,int(y_pos)))):
            path = x_axis[i] + str(j)
            valid_spots.append(path)
            if path == queen_pos or path == bishop_pos or path == rook_pos or path == knight_pos:
                break

        return valid_spots
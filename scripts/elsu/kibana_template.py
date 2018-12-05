# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:12:02 2018

@author: Okada
"""

def colors_32(i):

    colors = ["#57C17B",
        "#6F87D8",
        "#663DB8",
        "#BC52BC",
        "#9E3533",
        "#DAA05D",
        "#BFAF40",
        "#4050BF",
        "#BF5040",
        "#40AFBF",
        "#70BF40",
        "#8F40BF",
        "#BF40A7",
        "#40BF58",
        "#BF9740",
        "#4068BF",
        "#BF4048",
        "#40BFB7",
        "#87BF40",
        "#7840BF",
        "#BF4078",
        "#40BF87",
        "#B7BF40",
        "#4840BF",
        "#BF6840",
        "#4097BF",
        "#58BF40",
        "#A740BF",
        "#BF40B3",
        "#40BF4C",
        "#BF8B40",
        "#4074BF"
    ]
    return colors[(i<32) and i or i%32]
    
def main():
    pass

if __name__ == "__main__":
    pass


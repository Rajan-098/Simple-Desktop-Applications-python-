#developing this program has stopped due to inconvinience

class TruthTable():
    def __init__(self,variables):
        self.expression_format=False
        self.__variables=variables.upper()
        self.__var_len=len(self.__variables)
        self.__previous=" "
        self.__open=0
        self.__close=0
        self.__symbols=[ "<->" , "->" , "!" , "T" , "F" , "|" , "&" , "(" , ")" ]
        for var in self.__variables:
            self.__symbols.append(var)
        #print(self.__symbols)
        self.__temp_index=int(-1)
        self.__extracted_list=[]
        self.__skip_index=[-1]
        self.__parted_list=[]
        self.__parted_list_lite=[]
        self.__matched=False
    def check(self,inp):
        self.__inp=inp.upper()
        if len(str(self.__inp))==0:
            raise ValueError("String length must not be zero")
        elif not str(type(self.__inp))=="<class 'str'>":
            raise TypeError("TT expression must be 'str'")
        for letter in str(self.__inp):
            try:
                int(letter)
                raise ValueError("'int' is not available in TT expression ")
            except:
                pass
        for index,letter in enumerate(str(self.__inp)):
##            if letter == "-":
##                if self.__inp[index+1]==">":
##                    pass
##                else:
##                    raise ValueError("Invalid expression '-' Did you mean -> or <-> ?")
##            elif letter == "<":
##                if self.__inp[index+1]=="-" and self.__inp[index+2]==">":
##                    pass
##                else:
##                    raise ValueError("Invalid expression '<' Did you mean <-> ")
##            elif letter == ">":
##                if self.__inp[index-1]=="-":
##                    pass
##                else:
##                    raise ValueError("Invalid expression '>' Did you mean -> or <->")
##            else:
            if letter==self.__previous:
                raise TypeError("Invalid or empty expression, may be occured by string repeatation")
            self.__previous=letter
            if letter=="(":
                self.__open+=1
            elif letter==")":
                self.__close+=1
        if not self.__open==self.__close:
            raise TypeError("Mismatch of paranthesis")
        for index,inp_symbol in enumerate(self.__inp):
            if not index in self.__skip_index:
                self.__matched=False
                for predefined_symbol in self.__symbols:
                    if inp_symbol == predefined_symbol[0]:
                        #print( self.__inp[index:index+len (predefined_symbol)] )#[index, index + len (predefined_symbol)  ])
                        if self.__inp [index: index + len (predefined_symbol)  ] == predefined_symbol:
                            # this input symbol mvb atch exactly to the predefined_symbol
                            self.__matched=True
                            symbol=self.__inp[index:index+len(predefined_symbol)]
                            self.__extracted_list.append(symbol)
                            for for_index in range(len(predefined_symbol)-1):
                                self.__skip_index.append(index+for_index+1)
                        else:
                            raise ValueError(f"Incomplete symbol found, Did you mean {predefined_symbol}")
                if not self.__matched:
                    raise ValueError(f"'{inp_symbol}' does not match to any valid symbols")
                if symbol in self.__symbols:
                    print(self.__temp_index)
                    if not self.__symbols.index(symbol)==self.__temp_index:
                        self.__temp_index=self.__symbols.index(symbol)
                    else:
                        raise TypeError("Symbol of expression must not repeated")
                else:
                    raise ValueError("Unknown Symbol occured")
        return self.__extracted_list
    def __find_paranthesis(self,temp_list):
        self.temp_list=temp_list
        open_count=[]
        close_count=[]
        for index,variable in enumerate(self.temp_list):
            if variable=="(":
                open_count.append(index)
            elif variable==")":
                close_count.append(index)
                if len(close_count)==len(open_count):
                    self.__parted_list_lite.append(self.temp_list[open_count[0]:close_count[-1]+1])
                    """self.__parted_list_lite.append("""
                    self.__find_paranthesis(self.temp_list[open_count[0]+1:close_count[-1]-1])
                    #open_count.pop(0)
                    #close_count.pop(-1)
        #return self.temp_list
    def output(self):
        self.__parted_list.append(self.__extracted_list)
        self.__find_paranthesis(self.__extracted_list)
        for list_of in self.__parted_list_lite:
              print(list_of)

##        paranth=True
##        for start_index,variable1 in enumerate(self.__parted_list[0]):
##            if variable1=="(":
##                paranth=True
##                start=start_index
##                for end_index,variable2 in enumerate(self.__parted_list[0][::-1]):
##                    if variable2==")":
##                        end=len(self.__parted_list[0])-end_index
##                        if end>start:
##                            self.__parted_list.append(self.__parted_list[0][start:end])
##                            print(self.__parted_list)
##                        else:
##                            raise TypeError("Improper start of paranthesis")
tt=TruthTable("pqr")
print(tt.check("<->(<->->(<->(!))!->)->(<->)p"))
tt.output()

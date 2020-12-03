//
package main

func main(){
	b:= 15
	a:=0
	a = rec(b)
	print(a, "\n")
}

func rec(a int)(int){
	if a <= 0{
		return 0
	}else{
		b:=0
		b = a - 1
		print(b, "\n")
		a = rec(b) 
		return a
	}
}

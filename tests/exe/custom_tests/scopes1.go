//
package main

func main() {

	a := 4
	if a == 4{
		print("a je ", a, "\n")
		for i:= 0;i<4;i=i+1{
			a = a + 1
		}
		if a == 6{
			print("kurna co to je")
		}else{
			print("jede to: ", a)
			for i:=5;i>0;i = i-1{
				a = a + 1
				print("melo by byt 13, je: ", a, "\n")
				b := 0.0
				b = int2float(a)
				b = b + 0.4
				print("b je ", b)
				if a == 13{
					print("hraje tooo")
				}else{
					print("nehraje too")
				}
			}
		}
	}else{
		print("kurna co to je ")
	}
}
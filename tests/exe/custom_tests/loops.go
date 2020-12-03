//
package main

func loops(a int)(int){
	for i:=0;i<5;i=i+1{
		print("zacatek loopu", "\n")
		for j:=0;j<2;j=j+1{
			print("vnoreny loop \n")
			if j != 1{
				print("podminka 1")
			}else{
				print("else")
			}
		}
	}
   return a

}
func main() {

	b := 45
	a := 0 
	a = loops(b)
	print(a)
}

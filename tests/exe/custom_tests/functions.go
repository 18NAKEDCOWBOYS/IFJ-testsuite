//
package main

func constant()(int){
	return 25
}
func const2()(float64){
	return 12.5
}
func main() {

	a:=5
	b:=0.0
	c := 0
   c, b = func_calls(a)
   print(c, "\n")
   print(b, "\n")
}

func func_calls(a int)(int, float64){
   b:= 0.0
   b = const2()
   a = float2int(b)
   c := 0
   c = constant()
   d:=4
   if c == 25{
	   d = 1
   }else{
	   d = 2
   }
   print(a)
   print(b)
   print(c)
   print(d)
   return 10,11.2
}
; ModuleID = "hello"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"hello"()
{
entry:
  ret i32 37
}

; ModuleID = "hello"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"hello"()
{
entry:
  ret i32 37
}

define double @"dsquared"(double %".1", double %".2")
{
entry:
  %".4" = fmul double %".1", %".1"
  %".5" = fmul double %".2", %".2"
  %".6" = fadd double %".4", %".5"
  ret double %".6"
}

; ModuleID = "hello"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"hello"()
{
entry:
  ret i32 37
}

define double @"dsquared"(double %".1", double %".2")
{
entry:
  %".4" = fmul double %".1", %".1"
  %".5" = fmul double %".2", %".2"
  %".6" = fadd double %".4", %".5"
  ret double %".6"
}

declare double @"sqrt"(double %".1")

define double @"distance"(double %".1", double %".2")
{
entry:
  %".4" = call double @"dsquared"(double %".1", double %".2")
  %".5" = call double @"sqrt"(double %".4")
  ret double %".5"
}


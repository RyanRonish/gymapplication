#lang mystery-languages/arithmetic

(+ 1 1)
;; Basic arithmetic operations with exact integers, ssshould return 2
(- 1 1)
;; result should be 0
(* 1 1)
;; returns 1 as an exact integer
(/ 1 1)
;; division with exact integers, second language returns a float 
(// 1 1)
;;Failed floor division
(% 1 1)
;; one mod one should be zero

;; floating point numbers
;; (defvar x 0.1)
;; (defvar y 0.2)
;; (+ x y): 
;;          lang 1 will try to convert 0.1 and 0.2 to exact numbers if possible before addition.
;;          lang 2 will treat x and y as inexact and return a decimal value
;;          lang 3 will likely return an inexact floating-point result since x and y are inexact.

(defvar x 0.1)
(defvar x 0.1)
(defvar y 0.2)

(+ x y)

;; integer division
;; (defvar a 4)
;; (defvar b 2)
;; (defvar c 3)
;; (/ a b):
;;          lang 1 should return 2 as an exact integer (4/2 = 2).
;;          lang 2 should return 2.0 as an inexact floating-point number.
;;          lang 3 should return 2 as an exact integer since both operands are exact.
;; (/ a c):
;;          lang 1 should return 4/3 as an exact fraction.
;;          lang 2 should return approximately 1.3333333333333333 as an inexact floating-point number.
;;          lang 3 should return 4/3 as an exact fraction.

(defvar a 4)
(defvar b 2)
(defvar c 3)

(/ a b)
(/ a c)


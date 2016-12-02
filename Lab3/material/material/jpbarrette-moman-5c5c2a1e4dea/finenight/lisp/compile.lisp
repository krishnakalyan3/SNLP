(declaim (optimize (safety 0) (speed 3) (space 3) (debug 0)))
;(declaim (optimize (speed 0) (space 0) (compilation-speed 0) (debug 3)))

(compile-file "package.lisp")
(load "package")
(compile-file "utils.lisp")
(compile-file "fsa.lisp")
(compile-file "fsa-builder.lisp")
(compile-file "iadfa.lisp")
(compile-file "iadfa-run.lisp")


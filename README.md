# mal - Make a Lisp
[Original repo](https://github.com/kanaka/mal)
This is the biggest coding project i have ever completed.

In this repo, I undertook the mal process in python, to create a lisp
interpreter from scratch. I attempted the project three whole times, and due
to its scale and the amount I learned from the process, elected to start again
halfway through, finishing all the steps on attempt three. I have kept those
old implementations in their respective folders out of respect for the process,
but do not judge my coding ability from the code you find in there. I have also
purged the repo from code that isn't mine (bar the code needed to run the
tests). For more info on the mal project, please check out the original repo.

## My impls:
the folders that my implementations are in, in chronological order, are:
- mypythonold
- mypython
- synpy

synpy can pass all tests the mal repo has, provided you only run step A (the
older steps have some bugs). I may eventually make a new folder with each step
derived from the final working step, but seeing as the final test
`make MAL_IMPL=synpy "test^mal"` tests every step with the final file anyway,
this is not a priority.

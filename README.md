intcon
======

InteractiveConsole class reimplements raw_input

Copyright (c) 2013 Karol Tomala

# Usage:

    con = InteractiveConsole()
    print con('> ')

# Rationale:

Reimplementing raw_input might seem as a futile and unnecessary attempt, but there is
one special case where raw_input cannot be used. Since raw_input is a blocking call
there is no way to use it asynchronously in multithreaded console app like for example
interactive client to a server, where using curses is like taking sledgehammer to crack 
a nut. This was the primary reason for reimplementing raw_input behaviour.

Also with some additional work this class can be used with microthreads implementations.

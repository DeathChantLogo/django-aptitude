# the number of questions to render per test for each difficulty level.
# All of these values should add up to the total amount of questions you want
# the test to have overall.

D_QUESTIONS_COUNT = 10
C_QUESTIONS_COUNT = 15
B_QUESTIONS_COUNT = 25
A_QUESTIONS_COUNT = 50

# The total number of questions you can get wrong per difficulty level in order
# to achieve that grade. First value: questions you can miss in the previous
# difficulty level. The second number means how many you can miss in the
# current level. Since there is no level previous to D, it should be set to a
# single value (not a tuple). The grading algorythm already assumes you have
# already met all the prerequisites for all previous grades.

# to achieve a D grade, you must miss 0 D questions.
D_QUESTIONS_THRESHOLD = 0

# to achieve a C grade, you must miss 0 D's, and miss 3 or less C's.
C_QUESTIONS_THRESHOLD = (0, 3)

# to achieve a B grade, you must miss 1 or less C's, and miss 1 or less B's.
B_QUESTIONS_THRESHOLD = (1, 1)

# to achieve an A grade, you must miss 0 B's, and miss 25 or less A's.
A_QUESTIONS_THRESHOLD = (0, 25)

# the maximum amount of time that can pass after starting the test session
# where the test is still valid. EX: "30min", "34sec", "5hr40min30sec"
SESSION_OVERALL_TIMEOUT = "1hr"

# the maximum amount of time that can pass after starting the test session
# where getting an A grade is allowed. Used to ensure A grades don't go to
# people who may have cheated.
SESSION_A_GRADE_TIMEOUT = "45min"

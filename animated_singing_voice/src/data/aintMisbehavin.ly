\version "2.18.2"

\header {
  title = "AIN'T MISBEHAVIN’"
  composer = "Fats Waller/Harry Brooks"
  poet = "Andy Razaf"
}

global = {
  \key c \major
  \time 4/4
}

chordNames = \chordmode {
  \global
  % Akkorde folgen hier.
  
}

melody = \relative c' {
  \global
  \repeat volta 2 {
    r8 c d c g' g4.
    r8 d e d a'2
    r8 g a g c c4 b8
    d8 c a e~e es d4
    r8 c d c g' g4.
    r8 d e d a' a4 g8
     }
  \alternative {
    { e1~ e2 r }
    { c1~c2 r2 }
  }
  
  r4 c'8 a c a4.
  r4 c8 a c a4.
  r4 c8 a c a4.
  r4 cis8 a cis a4.
  r4 d d d
  d c b a
  g2 a
  e d
  
  r8 c d c g' g4.
  r8 d e d a'2
  r8 g a g c c4 b8
  d8 c a e~e es d4
  r8 c d c g' g4.
  r8 d e d a' a4 g8
  c1~ c2 r \bar "|."
  
  
}


\score {
  <<
    \new ChordNames \chordNames
    \new Staff { \melody }
  >>
  \layout { }
  \midi {
    \tempo 4=100
  }
}

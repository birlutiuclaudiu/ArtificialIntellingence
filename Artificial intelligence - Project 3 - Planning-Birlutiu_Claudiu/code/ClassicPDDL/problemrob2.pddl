(define (problem problemrob) 
(:domain robchemy)
(:objects 
    ep1 - eprubeta
    acid1 - acid
    baza1 - baza
    sare1 - sare
    berzelius1 - berzelius
    erlenmeyer1 - erlenmeyer
    left1  - left
    right1 - right
    ep2 - eprubeta
)

(:init
    ;paharele de masurat reactant
    (on-stativ berzelius1)
    (empty-clean berzelius1)
    (on-stativ erlenmeyer1)
    (empty-clean erlenmeyer1)

    ;;eprubete
    (on-stativ-e ep1)
    (not(empty-e ep1))
    (not (full-ep ep1))
    (on-stativ-e ep2)
    (empty-e ep2)
    (not (full-ep ep2))

    ;;bratele sunt libere
    (free-arm left1)
    (free-arm right1)
    ;;costul total
    (= (total-cost) 0)
)

(:goal (and
  
 (full-ep ep1)
 (result-precipitat ep1)

  (full-ep ep2)
  (result-sare ep2)
)

)
(:metric minimize ( total-cost) )

)
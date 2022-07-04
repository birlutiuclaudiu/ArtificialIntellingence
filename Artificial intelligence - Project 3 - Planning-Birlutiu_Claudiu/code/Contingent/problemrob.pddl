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
)

(:init
    ;paharele de masurat reactant
    (used berzelius1)
    (on-stativ berzelius1)
    (on-stativ erlenmeyer1)
    (used erlenmeyer1)

    ;;eprubete
    (on-stativ-e ep1)
    (empty-e ep1)
    
    (UNKNOWN (contains-s-rec acid1 berzelius1))
    (UNKNOWN (contains-s-rec baza1 erlenmeyer1))
    (UNKNOWN (contains-s-rec baza1 berzelius1))
    (UNKNOWN (contains-s-rec acid1 erlenmeyer1))

    (ONEOF  (contains-s-rec acid1 berzelius1)  (contains-s-rec baza1 berzelius1) )
    (ONEOF  (contains-s-rec acid1 erlenmeyer1) (contains-s-rec baza1 erlenmeyer1) )
    (ONEOF  (contains-s-rec acid1 berzelius1)  (contains-s-rec acid1 erlenmeyer1) )
    (ONEOF  (contains-s-rec baza1 berzelius1)  (contains-s-rec baza1 erlenmeyer1) )

    ;;bratele sunt libere
    (free-arm left1)
    (free-arm right1)
    ;;costul total
   
)

(:goal (and
  
;; (full-ep ep1)
;;(result-sare ep1)
;; (hold-e left1 ep1)
;; (full-ep ep2)
;; (result-sare ep2)
;;(contains-s-ep acid1 ep1);
 (AND (result-sare  ep1)
 )
)

)
)
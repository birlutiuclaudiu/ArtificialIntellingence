;; planificarea unui robot de a face reactii chimice

(define (domain robchemy)
    (:requirements :strips :typing :adl)

    (:types
        recipient reactant brat eprubeta        - object 
        left right                                        - brat
        berzelius erlenmeyer                              - recipient
        acid baza sare                                    - reactant
        
    )
    (:predicates 
        (free-arm ?a - brat     )                            ;;bratul e liber
        (empty-used ?r     - recipient)                      ;;recipientul e gol si nu a fost spalat
        (empty-clean ?r    - recipient)                      ;;recipientul e gol si curat
        (used ?r           - recipient)                          ;;recipientul e folosit si are ceva in el
        (hold ?a - brat ?r  - recipient)                     ;;in bratul a se afla recipientul r
        (on-stativ ?r      - recipient)                      ;;recipientul se afla pe stativ
        (contains-s-rec ?s - reactant ?r - recipient)        ;;un recipient contine substanta 
        (contains-s-ep ?s  - reactant ?e - eprubeta)         ;;eprubeta contine reactantul
        (empty-e ?e        - eprubeta)                       ;;eprubeta goala
        (hold-e ?a - brat ?e - eprubeta)                     ;;eprubeta e tinuta in brat
        (on-stativ-e ?e - eprubeta)             ;;eprubeta e pe stativ
        (full-ep ?e - eprubeta)                 ;;eprubeta e plina     
        (result-sare ?e - eprubeta)                 ;;reactie ACID + BAZA
        (result-baza-isnolubila ?e - eprubeta)      ;;reactie BAZA INSOLUBILA + SARE
        (result-precipitat ?e - eprubeta)           ;;reactie SARE +ACID

    )

   

    ;;ridicarea unui recipient in mana
    (:action gripp-recipient                             
        :parameters (?a - brat ?r - recipient)
        :precondition (and (free-arm ?a)     ;;sa fie liber bratul
                           (on-stativ ?r)    ;;recipientul sa fie pe stativ
                      )
        :effect (and (not (free-arm ?a))    ;;bratul nu va mai fi liber
                    (hold ?a ?r)            ;;bratul a tine recipientul r
                    (not (on-stativ ?r))    ;;recipientul nu mai e pe stativ
                  
                )
    )
   
    (:action senseContain
         :parameters (?s - reactant ?rec - recipient)
         :observe (contains-s-rec ?s ?rec)
   
   )
    ;;lasarea unui recipient pe masa
    (:action drop-recipient 
        :parameters (?a - brat ?r - recipient)
        :precondition (and (hold ?a ?r)   ;;implica faptul ca e mana ocupata si ca recipientul nu e pe stativ
                    )
        :effect (and  (not (hold ?a ?r))
                      (free-arm ?a)
                      (on-stativ ?r)
                    
        )
    )

    ;;masurarea unei cantitati de substanta; (introducerea ei intr-un pahar Berzelius sau Erlenmeyer)
    (:action measure-reactant                   ;;masurarea reactantului
        :parameters (?r - recipient ?s - reactant ?a1 ?a2 - brat)
        :precondition (and (hold ?a1 ?r)        ;;in mana sa avem recipientul de masurare
                           (free-arm ?a2)       ;;sa fie o mana libera pentru adaugarea reactantului 
                           (empty-clean ?r)     ;;sa fie curat si gol recipientul (sa nu apara reactii nedorite)
                      )
        :effect (and (contains-s-rec ?s ?r)    ;;substanta s se afla in recipientul r
                     (used ?r)
                     (not (empty-clean ?r))    ;;recipientul va contine ceva
                   
        )                
    )
    
    ;;adaugarea primului reactant in eprubeta
    (:action first-reactant 
        :parameters (?r - recipient ?s - reactant ?a1 - brat  ?a2 - brat ?e - eprubeta)   
        :precondition (and                             ;;presupune ca e plin paharul de masurat
                             (empty-e ?e)              ;;eprubeta trebuie sa fie goala pentru primul reactant
                             (hold ?a1 ?r)             ;;recipientul de masurat e in bratul robotului 
                             (not (full-ep ?e))        ;; nu e plina eprubeta
                             (hold-e ?a2 ?e)
                            (used ?r) 
                            (contains-s-rec ?s ?r)               ;;recipientul e plin cu substanta respectiva; adica nu e gol și a rămas nespalat
                        )
        :effect (and  (contains-s-ep ?s ?e )           ;;eprubeta contine reactantul s
                      (not (empty-e ?e))              ;;eprubeta nu mai e goala
                      (not (contains-s-rec ?s ?r))    ;;nu mai contine substanta recipientul
                      (empty-used ?r)                 ;;recipientul e empty-used (trebuie spalat daca se vrea masurarea altor substante)
                      (not (used ?r))
               )          
    )

    ;;adaugarea celui de-al doilea reactant in eprubeta si ultimul
    (:action second-reactant 
        :parameters (?r - recipient ?s - reactant ?a1 ?a2 - brat  ?e - eprubeta)   
        :precondition (and  
                            (hold ?a1 ?r)             ;;recipientul de masurat e in bratul robotului 
                            ;(exists (?s1 - reactant) (and (not (= ?s1 ?s)) (contains-s-ep ?s1 ?e) ));;nu se adauga aceeasi substanta
                            (not (full-ep ?e))        ;; nu e plina eprubeta
                            (hold-e ?a2 ?e)           ;;eprrubeta e tinuta in brat pentru a adauga substanta
                            (not (empty-e ?e))        ;;eprubeta contine primul reactant
                            (used ?r) 
                            (contains-s-rec ?s ?r)               ;;recipientul e plin cu substanta respectiva; adica nu e gol și a rămas nespalat
                        )                                              
                        
        :effect (and    (contains-s-ep ?s ?e )             ;;eprubeta contine reactantul s
                        (full-ep ?e)                       ;;eprubeta e plina
                        (not (contains-s-rec ?s ?r))       ;;nu mai contine substanta recipientul
                        (empty-used ?r)                    ;;recipientul e empty-used (trebuie spalata daca se vrea masurarea altor substante)          
                )         
    )

    ;;curatarea recipientului
    (:action clean-recipient
        :parameters (?r - recipient ?a - brat)
        :precondition (and ;(empty-used ?r)
                           (hold ?a ?r)       ;;trebuie sa fie in mana recipientul pt a fi spalat
                      )
        :effect (and (empty-clean ?r)
                (not (empty-used ?r))   
                (not (used ?r))   
                (forall (?s - reactant) (when (and (contains-s-rec ?s ?r)) (not (contains-s-rec ?s ?r) )))   ;;se vor goli si substantele din recipient 
        )
    )

    ;;clean eprubeta
    (:action clean-eprubeta
        :parameters (?e - eprubeta ?a - brat)
        :precondition (and (not (empty-e ?e))   ;;sa nu o spele degeaba
                           (hold-e ?a ?e)       ;;sa aiba eprubeta in brat
                    )
        :effect (and (empty-e ?e)
                (not (full-ep ?e))
                (forall (?s - reactant) (when (and (contains-s-ep ?s ?e)) (not (contains-s-ep ?s ?e) )))   ;;se vor goli si substantele din ea 
                (not (result-sare ?e));
                (not (result-baza-isnolubila ?e))  ;;golirea eprubetei
                (not (result-precipitat ?e ))   
               
        )
    )
    ;;ia eprubeta in brat
    (:action gripp-eprubeta
        :parameters (?e - eprubeta ?a - brat)
        :precondition (and (on-stativ-e ?e)
                            (free-arm ?a)
                      )
        :effect(and (not (on-stativ-e ?e))
                    (hold-e ?a ?e)      ;;e in mana 
                    (not (free-arm ?a))
                    
                )
    )

    ;;lasa eprubeta pe stativ 
    (:action drop-eprubeta
        :parameters (?e - eprubeta ?a - brat)
        :precondition (and (hold-e ?a ?e)
                      )
        :effect(and (on-stativ-e ?e)
                    (not (hold-e ?a ?e))      ;;e pe stativ 
                    (free-arm ?a)
                   
                )
    )

     ;;verificare rezultat reactie 
    (:action check-reactie-baza-acid
        :parameters (?e - eprubeta)
        :precondition (and (full-ep ?e)
                        (exists (?s - baza) (and (contains-s-ep ?s ?e) ))
                        (exists (?s - acid) (and (contains-s-ep ?s ?e) ))

        )
        :effect (and (result-sare ?e))
    )

     ;;verificare rezultat reactie 
    (:action check-reactie-baza-sare
        :parameters (?e - eprubeta)
        :precondition (and (full-ep ?e)
                        (exists (?s - baza) (and (contains-s-ep ?s ?e) ))
                        (exists (?s - sare) (and (contains-s-ep ?s ?e) ))

        )
        :effect (and (result-baza-isnolubila ?e))
    )

     ;;verificare rezultat reactie 
    (:action check-reactie-acid-sare
        :parameters (?e - eprubeta)
        :precondition (and (full-ep ?e)
                        (exists (?s - sare) (and (contains-s-ep ?s ?e) ))
                        (exists (?s - acid) (and (contains-s-ep ?s ?e) ))

        )
        :effect (and (result-precipitat ?e) )
    )
    
    

   
)
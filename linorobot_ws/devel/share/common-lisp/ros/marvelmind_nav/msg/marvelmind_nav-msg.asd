
(cl:in-package :asdf)

(defsystem "marvelmind_nav-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "beacon_pos_a" :depends-on ("_package_beacon_pos_a"))
    (:file "_package_beacon_pos_a" :depends-on ("_package"))
    (:file "hedge_pos" :depends-on ("_package_hedge_pos"))
    (:file "_package_hedge_pos" :depends-on ("_package"))
    (:file "hedge_pos_a" :depends-on ("_package_hedge_pos_a"))
    (:file "_package_hedge_pos_a" :depends-on ("_package"))
  ))
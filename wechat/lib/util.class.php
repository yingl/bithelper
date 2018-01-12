<?php

class Util {
    private $dao;

    public function __construct($dao) {
        $this->dao = $dao;
    }

    public function fetch_code($code) {
        $query = 'select * from btc_values where code = ? order by updated_at desc limit 1';
        $info = $this->dao->execute_with_fetch($query, array($code));
        return $info[0];
    }
    
    public function fetch_tops() {
        $query = 'select * from btc_tops order by updated_at desc linit 1';
        $info = $this->dao->execute_with_fetch($query);
        return $info[0];
    }
    
    public function fetch_bottoms() {
        $query = 'select * from btc_bottoms order by updated_at desc linit 1';
        $info = $this->dao->execute_with_fetch($query);
        return $info[0];
    }
}

?>

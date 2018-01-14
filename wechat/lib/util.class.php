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

    public function fetch_aggs($tag) {
        $query = 'select * from btc_aggs where tag = ? order by updated_at desc limit 1';
        $info = $this->dao->execute_with_fetch($query, array($tag));
        return $info[0];
    }
}

?>

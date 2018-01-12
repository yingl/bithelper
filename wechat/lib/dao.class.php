<?php

class DAO {
    private $dbh;
    private $stmt;

    public function __construct($options) {
        try {
            $this->dbh = new PDO($options['dsn'],
                                 $options['username'],
                                 $options['password'],
                                 $options['options']);
            $this->dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        }
        catch (PDOException $e) {
            die($e->getMessage());
        }
    }

    public function execute($query, $values=array()) {
        $this->stmt = $this->dbh->prepare($query);
        if (count($values) > 0) {
            $this->stmt->execute($values);  
        }
        else {
                $this->stmt->execute(); 
        }
        return $this->stmt;
    }

    public function execute_with_fetch($query, $values=array()) {
        $this->execute($query, $values);
        return $this->stmt->fetchAll();
    }

    public function get_affected_rows() {
        return $this->stmt->rowCount();
    }

    public function begin_transaction() {
        $this->dbh->beginTransaction();
    }

    public function commit() {
        $this->dbh->commit();
    }

    public function roll_back() {
        $this->dbh->rollBack();
    }
}

?>

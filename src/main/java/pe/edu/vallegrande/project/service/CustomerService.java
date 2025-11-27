package pe.edu.vallegrande.project.service;

import java.util.List;
import java.util.Optional;

import pe.edu.vallegrande.project.model.Customer;

public interface CustomerService {

    List<Customer> findAll();

    Optional<Customer> findById(Long id);

    Customer save(Customer customer);

    Customer update(Customer customer);

    void delete(Long id);

    byte[] generateJasperPdfReport() throws Exception;
}

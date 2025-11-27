package pe.edu.vallegrande.project.service;

import java.util.List;
import java.util.Optional;

import pe.edu.vallegrande.project.model.Supplier;

public interface SupplierService {
    List<Supplier> findAll();
    Optional<Supplier> findById(Integer id);
    Supplier save(Supplier supplier);
    Supplier update(Supplier supplier);
    void delete(Integer id);
    byte[] generateJasperPdfReport() throws Exception;
}

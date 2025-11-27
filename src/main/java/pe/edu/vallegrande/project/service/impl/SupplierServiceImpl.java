package pe.edu.vallegrande.project.service.impl;

import java.io.InputStream;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;

import javax.sql.DataSource;

import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import lombok.extern.slf4j.Slf4j;
import net.sf.jasperreports.engine.JasperExportManager;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import pe.edu.vallegrande.project.model.Supplier;
import pe.edu.vallegrande.project.repository.SupplierRepository;
import pe.edu.vallegrande.project.service.SupplierService;

@Slf4j
@Service
public class SupplierServiceImpl implements SupplierService {

    private final SupplierRepository supplierRepository;
    private final DataSource dataSource;

    // Constructor con ambos parámetros
    public SupplierServiceImpl(SupplierRepository supplierRepository, DataSource dataSource) {
        this.supplierRepository = supplierRepository;
        this.dataSource = dataSource;
    }

    @Override
    public List<Supplier> findAll() {
        log.info("Listando proveedores");
        return supplierRepository.findAll();
    }

    @Override
    public Optional<Supplier> findById(Integer id) {
        log.info("Buscando proveedor por ID: {}", id);
        return supplierRepository.findById(id);
    }

    @Override
    public Supplier save(Supplier supplier) {
        if (supplier.getStatus() == null) {
            supplier.setStatus("A");
        }
        if (supplier.getRegistrationDate() == null) {
            supplier.setRegistrationDate(LocalDate.now());
        }
        return supplierRepository.save(supplier);
    }

    @Override
    public Supplier update(Supplier supplier) {
        log.info("Actualizando proveedor: {}", supplier);
        return supplierRepository.save(supplier);
    }

    @Override
    public void delete(Integer id) {
        log.info("Eliminando proveedor con ID: {}", id);
        supplierRepository.deleteById(id);
    }

    @Override
    public byte[] generateJasperPdfReport() throws Exception {
        // Cargar archivo .jasper en src/main/resources/reports (SIN USAR IMÁGENES EN EL
        // JASPER)
        InputStream jasperStream = new ClassPathResource("reports/supplierReport.jasper").getInputStream();
        // Sin parámetros
        HashMap<String, Object> params = new HashMap<>();
        // Llenar reporte con conexión a Oracle Cloud con application.yml |
        // aplicación.properties
        JasperPrint jasperPrint = JasperFillManager.fillReport(jasperStream, params, dataSource.getConnection());
        // Exportar a PDF
        return JasperExportManager.exportReportToPdf(jasperPrint);
    }
}
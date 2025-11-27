package pe.edu.vallegrande.project.service.impl;

import java.io.InputStream;
import java.sql.Connection;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;
import javax.sql.DataSource;
import org.springframework.core.io.ClassPathResource;
import lombok.extern.slf4j.Slf4j;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import net.sf.jasperreports.engine.JasperExportManager;
import pe.edu.vallegrande.project.model.Customer;
import pe.edu.vallegrande.project.repository.CustomerRepository;
import pe.edu.vallegrande.project.service.CustomerService;

@Slf4j
@Service
public class CustomerServiceImpl implements CustomerService {

    private final CustomerRepository customerRepository;
    private final DataSource dataSource;

    public CustomerServiceImpl(CustomerRepository customerRepository, DataSource dataSource) {
        this.customerRepository = customerRepository;
        this.dataSource = dataSource;
    }

    @Override
    public List<Customer> findAll() {
        log.info("Listando Datos: ");
        return customerRepository.findAll();
    }

    @Override
    public Optional<Customer> findById(Long id) {
        log.info("Listando Datos por ID: ");
        return customerRepository.findById(id);
    }

    @Override
    public Customer save(Customer customer) {
        log.info("Registrando Datos: " + customer.toString());
        return customerRepository.save(customer);
    }

    @Override
    public Customer update(Customer customer) {
        log.info("Editando Datos: " + customer.toString());
        return customerRepository.save(customer);
    }

    @Override
    public void delete(Long id) {
        customerRepository.deleteById(id);
    }


@Override
public byte[] generateJasperPdfReport() throws Exception {
    log.info("Generando reporte Jasper PDF");
    try (InputStream jasperStream = new ClassPathResource("reports/customer.jasper").getInputStream();
         Connection conn = dataSource.getConnection()) {
        HashMap<String, Object> params = new HashMap<>();
        JasperPrint jasperPrint = JasperFillManager.fillReport(jasperStream, params, conn);
        return JasperExportManager.exportReportToPdf(jasperPrint);
    } catch (Exception e) {
        log.error("Error generando reporte Jasper PDF", e);
        throw e; // O envuelve en una excepción personalizada
    }
}
}

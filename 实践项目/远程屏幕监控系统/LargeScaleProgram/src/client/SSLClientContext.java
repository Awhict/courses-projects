package client;

import javax.net.ssl.*;
import java.io.FileInputStream;
import java.security.KeyStore;

public class SSLClientContext {

    private static final String KEYSTORE_PATH = "CLIENT\\clientkeystore.jks";
    private static final String KEYSTORE_PASSWORD = "password";
    private static final String TRUSTSTORE_PATH = "CLIENT\\clienttruststore.jks";
    private static final String TRUSTSTORE_PASSWORD = "password";

    public static SSLContext getSSLContext() throws Exception {
        // Load client keystore
        KeyStore clientKeyStore = KeyStore.getInstance("JKS");
        clientKeyStore.load(new FileInputStream(KEYSTORE_PATH), KEYSTORE_PASSWORD.toCharArray());

        // Load client truststore
        KeyStore trustStore = KeyStore.getInstance("JKS");
        trustStore.load(new FileInputStream(TRUSTSTORE_PATH), TRUSTSTORE_PASSWORD.toCharArray());

        // Initialize key manager factory
        KeyManagerFactory keyManagerFactory = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
        keyManagerFactory.init(clientKeyStore, KEYSTORE_PASSWORD.toCharArray());

        // Initialize trust manager factory
        TrustManagerFactory trustManagerFactory = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        trustManagerFactory.init(trustStore);

        // Create SSL context
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(keyManagerFactory.getKeyManagers(), trustManagerFactory.getTrustManagers(), null);

        return sslContext;
    }
}

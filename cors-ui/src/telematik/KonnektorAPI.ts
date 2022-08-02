import axios, { AxiosInstance, AxiosResponse } from "axios";

export class KonnektorConfig {
    constructor(
        public url: string, 
        public username: string,
        public password: string,
        public mandantId: string, 
        public clientSystemId: string, 
        public workplaceId: string) {}
}

export class KonnektorAPI {
    konnektorConfig: KonnektorConfig;
    axios: AxiosInstance;

    constructor(konnektorConfig: KonnektorConfig) {
        this.konnektorConfig = konnektorConfig
        this.axios = axios.create(
            {
                headers: {
                    "Authorization": "Basic " + btoa(this.konnektorConfig.username + ":" + this.konnektorConfig.password)
                }
            }            
        )
    }

    getServices() {
        return this.axios.get(
            this.konnektorConfig.url+"/connector.sds")
    }

    getCards() {
        let body = `<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
        <soap-env:Body>
            <ns0:GetCards xmlns:ns0="http://ws.gematik.de/conn/EventService/v7.2" mandant-wide="false">
            <ns1:Context xmlns:ns1="http://ws.gematik.de/conn/ConnectorContext/v2.0">
                <ns2:MandantId xmlns:ns2="http://ws.gematik.de/conn/ConnectorCommon/v5.0">MandantId</ns2:MandantId>
                <ns3:ClientSystemId xmlns:ns3="http://ws.gematik.de/conn/ConnectorCommon/v5.0">ClientSystemId</ns3:ClientSystemId>
                <ns4:WorkplaceId xmlns:ns4="http://ws.gematik.de/conn/ConnectorCommon/v5.0">WorkplaceId</ns4:WorkplaceId>
            </ns1:Context>
            </ns0:GetCards>
        </soap-env:Body>
        </soap-env:Envelope>`
        return this.axios.post(
            this.konnektorConfig.url+"/soap-api/EventService/7.2.0",
            body,
            {
            headers: {
                SOAPAction: "http://ws.gematik.de/conn/EventService/v7.2#GetCards",
                Accept: "application/xml",
            },
            },
        )        
    }

}
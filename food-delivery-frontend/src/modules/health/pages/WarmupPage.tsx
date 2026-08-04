import {
  Button,
  Center,
  Container,
  Stack,
  Text,
} from "@mantine/core";

import { useNavigate } from "react-router-dom";

import { useSystemStatus } from "../hooks/useSystemStatus";
import ServiceStatusCard from "../components/ServiceStatusCard";


export default function WarmupPage() {
  const navigate = useNavigate();

  const {
    data,
    isPending,
    refetch,
  } = useSystemStatus();


  const ready = data?.ready ?? false;


  return (
    <Center mih="100vh">

      <Container size="sm" w="100%">

        <Stack>

          <Text
            size="xl"
            fw={700}
          >
            System Status
          </Text>


          {isPending && (
            <Text>
              Checking services...
            </Text>
          )}


          {data?.services.map((service) => (
            <ServiceStatusCard
              key={service.name}
              service={service}
            />
          ))}


          <Button
            onClick={() => refetch()}
          >
            Check Again
          </Button>


          <Button
            disabled={!ready}
            onClick={() => navigate("/login")}
          >
            Continue
          </Button>


        </Stack>

      </Container>

    </Center>
  );
}
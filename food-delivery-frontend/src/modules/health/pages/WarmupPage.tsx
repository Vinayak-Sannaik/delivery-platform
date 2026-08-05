import {
  Button,
  Center,
  Container,
  Stack,
  Text,
} from "@mantine/core";

import { useNavigate } from "react-router-dom";

import { useWarmup } from "../hooks/useWarmup";
import ServiceStatusCard from "../components/ServiceStatusCard";


export default function WarmupPage() {
  const navigate = useNavigate();

  const {
    mutate,
    data,
    isPending,
  } = useWarmup();


  const ready = data?.ready ?? false;


  return (
    <Center mih="100vh">

      <Container size="sm" w="100%">

        <Stack>

          <Text
            size="xl"
            fw={700}
          >
            Food Delivery Platform
          </Text>


          {ready?<Text c="green">
            All backend services are ready.
          </Text> : <Text c="dimmed">
            Wake all backend services before using the application.
          </Text>}


          {data?.services.map((service) => (
            <ServiceStatusCard
              key={service.name}
              service={service}
            />
          ))}

          
          


          <Button
  loading={isPending}
  disabled={ready}
  onClick={() => mutate()}
>
  {ready ? "Application Ready" : "Start Application"}
</Button>


          <Button
            disabled={!ready}
            onClick={() => navigate("/login")}
          >
            Continue to Login
          </Button>


        </Stack>

      </Container>

    </Center>
  );
}
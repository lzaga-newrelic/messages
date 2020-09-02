emulator_host = 'localhost:8085'


if __name__ == "__main__":
    from messages.server import MessagesServer

    service_factory = MessagesServer()

    (
        service_factory.bind_ioloop()
            .define_logger(development=True)
            .register_curl_client()
            .bind_dependencies()
            .add_pubsub_handlers()
            .create_pubsub_app(emulator_host=emulator_host)
            .add_routes()
            .create_app()
            .start_server()
    )

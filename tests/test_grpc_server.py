import pytest

# Start the tests via `make test-debug` or `make test-release`


async def test_grpc_client(hello_protos, mock_grpc_hello, grpc_service):
    @mock_grpc_hello('SayHello')
    async def mock_say_hello(request, context):
        return hello_protos.HelloResponse(
            text=f'{request.name}!!',
        )

    request = hello_protos.HelloRequest(name='mock_userver')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hello, userver!!!\n'
    assert mock_say_hello.times_called == 1


async def test_first_time_users(hello_protos, grpc_service):
    request = hello_protos.HelloRequest(name='userver')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hello, userver!\n'


async def test_db_updates(hello_protos, grpc_service):
    request = hello_protos.HelloRequest(name='World')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hello, World!\n'

    request = hello_protos.HelloRequest(name='World')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hi again, World!\n'

    request = hello_protos.HelloRequest(name='World')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hi again, World!\n'


@pytest.mark.pgsql('db-1', files=['initial_data.sql'])
async def test_db_initial_data(hello_protos, grpc_service):
    request = hello_protos.HelloRequest(name='user-from-initial_data.sql')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hi again, user-from-initial_data.sql!\n'

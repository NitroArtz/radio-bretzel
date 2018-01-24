import docker
client = docker.from_env()
volume = client.volume.create(name='audio',
                              driver='local',
                              )


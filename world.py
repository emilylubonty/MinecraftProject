from settings import *
from world_objects.chunk import Chunk
from voxel_handler import VoxelHandler


class World:
    def __init__(self, app):
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)

    def update(self):
        self.voxel_handler.update()

    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # put the chunk voxels in a separate array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # get pointer to voxels
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def render(self):
        for chunk in self.chunks:
            chunk.render()
    def get_terrain_height(self, x, z):
        # Find the chunk and exact position within the chunk
        chunk_x, chunk_z = x // CHUNK_SIZE, z // CHUNK_SIZE
        local_x, local_z = x % CHUNK_SIZE, z % CHUNK_SIZE
        chunk_index = chunk_x + WORLD_W * chunk_z  # Simplified index

        # Get height within this chunk at (local_x, local_z)
        if 0 <= chunk_index < len(self.chunks) and self.chunks[chunk_index]:
            return self.chunks[chunk_index].get_height(local_x, local_z)
        else:
            return 0  # Default ground level if outside bounds
FROM golang:1.22-alpine AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN go build -o /stonescan ./cmd/server

FROM alpine:3.19
COPY --from=build /stonescan /stonescan
ENTRYPOINT ["/stonescan"]
